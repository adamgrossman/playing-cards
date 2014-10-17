from django.test import TestCase
from cards.models import Card


class get_war_result(TestCase):
    def setUp(self):
        self.card_one = Card.objects.create(suit=Card.CLUB, rank="three")
        self.card_two = Card.objects.create(suit=Card.CLUB, rank="two")
        self.card_three = Card.objects.create(suit=Card.CLUB, rank="three")

    def test_get_war_result(self):
        self.assertEqual(self.card_one.get_war_result(self.card_two), 1)
        self.assertEqual(self.card_one.get_war_result(self.card_three), 0)
        self.assertEqual(self.card_two.get_war_result(self.card_three), -1)
