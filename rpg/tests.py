from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Roll, Ruleset
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
            {'label': 'Attack', 'expression': '1d20+2', 'ruleset': ruleset.slug},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Roll.objects.filter(user=user, ruleset=ruleset).count(), 1)
