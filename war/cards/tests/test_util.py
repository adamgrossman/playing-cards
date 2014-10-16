from django.test import TestCase
from cards.models import Card
from cards.utils import create_deck


class UtilTestCase(TestCase):
    def test_create_deck_count(self):
        """Test that we created 52 cards"""
        create_deck()
        self.assertEqual(Card.objects.count(), 52)
