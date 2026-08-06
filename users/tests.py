from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class UserAuthTests(TestCase):
    def test_login_page_renders_dedicated_form(self):
        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Twoja kampania czeka.')
        self.assertContains(response, 'Nazwa użytkownika')
        self.assertContains(response, 'Wejdź do gry')

    def test_login_page_shows_clear_error_for_invalid_credentials(self):
        response = self.client.post(
            reverse('login'),
            {'username': 'nieznany', 'password': 'bledne-haslo'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nie udało się zalogować.')

    def test_user_password_is_hashed_once(self):
        user = get_user_model().objects.create_user(username='player', password='strong-pass-123')

        self.assertTrue(user.check_password('strong-pass-123'))

    def test_profile_api_returns_current_user(self):
        user = get_user_model().objects.create_user(
            username='player',
            email='player@example.com',
            password='strong-pass-123',
        )
        self.client.force_login(user)

        response = self.client.get(reverse('api-profile'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['username'], 'player')

    def test_user_can_update_profile_role(self):
        user = get_user_model().objects.create_user(username='player', password='strong-pass-123')
        self.client.force_login(user)

        response = self.client.post(
            reverse('profile'),
            {
                'username': 'player',
                'email': '',
                'first_name': '',
                'last_name': '',
                'profile_role': 'game_master',
            },
        )

        self.assertRedirects(response, reverse('profile'))
        user.refresh_from_db()
        self.assertEqual(user.profile_role, 'game_master')
