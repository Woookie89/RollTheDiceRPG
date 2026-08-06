from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Campaign, Character, JournalEntry, Roll, Ruleset
from .services.dice import roll_expression


class DiceTests(TestCase):
    def test_roll_expression_returns_roll_parts(self):
        result = roll_expression('2d6+3')

        self.assertEqual(len(result['rolls']), 2)
        self.assertEqual(result['modifier'], 3)
        self.assertGreaterEqual(result['total'], 5)
        self.assertLessEqual(result['total'], 15)


class DashboardRollTests(TestCase):
    def test_logged_user_can_create_roll_from_dashboard(self):
        user = get_user_model().objects.create_user(username='player', password='strong-pass-123')
        ruleset = Ruleset.objects.get(slug='dnd5e')
        self.client.force_login(user)

        response = self.client.post(
            reverse('roll-create'),
            {'label': 'Atak', 'context': 'mieczem', 'expression': '1d20+2', 'ruleset': ruleset.slug},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Roll.objects.filter(user=user, ruleset=ruleset).count(), 1)
        self.assertEqual(Roll.objects.get(user=user).context, 'mieczem')

    def test_htmx_roll_returns_result_partial(self):
        user = get_user_model().objects.create_user(username='player', password='strong-pass-123')
        ruleset = Ruleset.objects.get(slug='dnd5e')
        self.client.force_login(user)

        response = self.client.post(
            reverse('roll-create'),
            {'preset': 'dnd-test', 'expression': '1d4', 'ruleset': ruleset.slug},
            HTTP_HX_REQUEST='true',
        )

        self.assertContains(response, 'Test d20')
        self.assertContains(response, 'Kości:')

    def test_dashboard_renders_polish_empty_states(self):
        user = get_user_model().objects.create_user(username='player', password='strong-pass-123')
        self.client.force_login(user)

        response = self.client.get(reverse('dashboard'))

        self.assertContains(response, 'Twój pulpit RPG')
        self.assertContains(response, 'Utwórz pierwszą postać')
        self.assertContains(response, 'Ustaw rolę MG')


class CharacterFlowTests(TestCase):
    def test_character_form_saves_system_data(self):
        user = get_user_model().objects.create_user(username='player', password='strong-pass-123')
        ruleset = Ruleset.objects.get(slug='dnd5e')
        self.client.force_login(user)

        response = self.client.post(
            reverse('character-create'),
            {
                'name': 'Lena',
                'ruleset': ruleset.slug,
                'campaign': '',
                'role': 'Wojowniczka',
                'origin': 'Strażniczka traktu',
                'level': '3',
                'resource': '17',
                'health': '24',
                'notes': 'Chroni drużynę.',
            },
        )

        character = Character.objects.get(owner=user, name='Lena')
        self.assertRedirects(response, reverse('character-detail', kwargs={'pk': character.pk}))
        self.assertEqual(character.data['role']['label'], 'Klasa')
        self.assertEqual(character.data['role']['value'], 'Wojowniczka')
        self.assertEqual(character.data['default_expression'], '1d20')

    def test_character_detail_view_renders_html(self):
        user = get_user_model().objects.create_user(username='player', password='strong-pass-123')
        ruleset = Ruleset.objects.get(slug='dnd5e')
        character = Character.objects.create(owner=user, ruleset=ruleset, name='Lena')
        self.client.force_login(user)

        response = self.client.get(reverse('character-detail', kwargs={'pk': character.pk}))

        self.assertContains(response, 'Karta postaci')
        self.assertContains(response, 'Lena')

    def test_user_cannot_edit_other_user_character(self):
        owner = get_user_model().objects.create_user(username='owner', password='strong-pass-123')
        intruder = get_user_model().objects.create_user(username='intruder', password='strong-pass-123')
        ruleset = Ruleset.objects.get(slug='dnd5e')
        character = Character.objects.create(owner=owner, ruleset=ruleset, name='Lena')
        self.client.force_login(intruder)

        response = self.client.post(
            reverse('character-edit', kwargs={'pk': character.pk}),
            {'name': 'Changed', 'ruleset': ruleset.slug},
        )

        self.assertEqual(response.status_code, 404)
        character.refresh_from_db()
        self.assertEqual(character.name, 'Lena')

    def test_browser_api_character_detail_redirects_to_html_view(self):
        user = get_user_model().objects.create_user(username='player', password='strong-pass-123')
        ruleset = Ruleset.objects.get(slug='dnd5e')
        character = Character.objects.create(owner=user, ruleset=ruleset, name='Lena')
        self.client.force_login(user)

        response = self.client.get(
            reverse('character-detail', kwargs={'pk': character.pk}).replace('/characters/', '/api/characters/'),
            HTTP_ACCEPT='text/html',
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], reverse('character-detail', kwargs={'pk': character.pk}))


class JournalTests(TestCase):
    def test_logged_user_can_create_journal_entry(self):
        user = get_user_model().objects.create_user(username='player', password='strong-pass-123')
        ruleset = Ruleset.objects.get(slug='dnd5e')
        campaign = Campaign.objects.create(owner=user, ruleset=ruleset, name='Cienie nad portem')
        self.client.force_login(user)

        response = self.client.post(
            reverse('journal-create'),
            {
                'title': 'Pierwszy trop',
                'entry_type': JournalEntry.NOTE,
                'campaign': campaign.pk,
                'character': '',
                'body': 'Kupiec widział dziwny symbol.',
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(JournalEntry.objects.filter(user=user, campaign=campaign).count(), 1)

    def test_api_journal_rejects_other_user_campaign(self):
        owner = get_user_model().objects.create_user(username='owner', password='strong-pass-123')
        intruder = get_user_model().objects.create_user(username='intruder', password='strong-pass-123')
        ruleset = Ruleset.objects.get(slug='dnd5e')
        campaign = Campaign.objects.create(owner=owner, ruleset=ruleset, name='Cienie nad portem')
        self.client.force_login(intruder)

        response = self.client.post(
            reverse('api-journal-list'),
            {
                'title': 'Nie mój wpis',
                'entry_type': JournalEntry.NOTE,
                'campaign': campaign.pk,
                'body': 'Próba zapisu.',
            },
        )

        self.assertEqual(response.status_code, 403)
        self.assertFalse(JournalEntry.objects.filter(title='Nie mój wpis').exists())

    def test_browser_api_campaign_detail_redirects_to_html_view(self):
        user = get_user_model().objects.create_user(username='player', password='strong-pass-123')
        ruleset = Ruleset.objects.get(slug='dnd5e')
        campaign = Campaign.objects.create(owner=user, ruleset=ruleset, name='Cienie nad portem')
        self.client.force_login(user)

        response = self.client.get(
            reverse('campaign-detail', kwargs={'pk': campaign.pk}).replace('/campaigns/', '/api/campaigns/'),
            HTTP_ACCEPT='text/html',
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], reverse('campaign-detail', kwargs={'pk': campaign.pk}))


class LandingTests(TestCase):
    def test_landing_renders_polish_copy_and_rulesets(self):
        response = self.client.get(reverse('landing'))

        self.assertContains(response, 'Wielosystemowy stół RPG')
        self.assertContains(response, 'Dungeons &amp; Dragons 5E')
        self.assertContains(response, 'Tajemnice Pętli i Powodzi')


class UserRoleTests(TestCase):
    def test_player_cannot_create_campaign_from_ui(self):
        user = get_user_model().objects.create_user(username='player', password='strong-pass-123')
        self.client.force_login(user)

        response = self.client.get(reverse('campaign-create'))

        self.assertRedirects(response, reverse('profile'))

    def test_game_master_can_create_campaign_from_ui(self):
        user = get_user_model().objects.create_user(
            username='gm',
            password='strong-pass-123',
            profile_role='game_master',
        )
        ruleset = Ruleset.objects.get(slug='dnd5e')
        self.client.force_login(user)

        response = self.client.post(
            reverse('campaign-create'),
            {'name': 'Cienie nad portem', 'ruleset': ruleset.slug, 'description': ''},
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Campaign.objects.filter(owner=user, name='Cienie nad portem').exists())
