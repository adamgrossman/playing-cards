from django.test import TestCase
from cards.models import WarGame, Player, Card
from cards.tests.factories import WarGameFactory


class ModelTestCase(TestCase):
    def setUp(self):
        self.card = Card.objects.create(suit=Card.CLUB, rank="jack")

    def create_war_game(self, user, result=WarGame.LOSS):
        WarGame.objects.create(result=result, player=user)

    def test_get_ranking(self):
        """Test that we get the proper ranking for a card"""
        self.assertEqual(self.card.get_ranking(), 11)

    def test_get_war_result_greater(self):
        first_card = Card.objects.create(suit=Card.DIAMOND, rank="five")
        second_card = Card.objects.create(suit=Card.DIAMOND, rank="four")
        self.assertEqual(first_card.get_war_result(second_card), 1)

    def test_get_war_result_equal(self):
        first_card = Card.objects.create(suit=Card.DIAMOND, rank="five")
        second_card = Card.objects.create(suit=Card.DIAMOND, rank="five")
        self.assertEqual(first_card.get_war_result(second_card), 0)

    def test_get_war_result_less(self):
        first_card = Card.objects.create(suit=Card.DIAMOND, rank="four")
        second_card = Card.objects.create(suit=Card.DIAMOND, rank="five")
        self.assertEqual(first_card.get_war_result(second_card), -1)

    def test_get_wins(self):
        user = Player.objects.create_user(username='test-user', email='test@test.com', password='password')
        WarGameFactory.create_batch(2, player=user, result=WarGame.WIN)
        self.assertEqual(user.get_wins(), 2)

    def test_get_losses(self):
        user = Player.objects.create_user(username='test-user', email='test@test.com', password='password')
        WarGameFactory.create_batch(3, player=user, result=WarGame.LOSS)
        self.assertEqual(user.get_losses(), 3)

    def test_get_ties(self):
        user = Player.objects.create_user(username='test-user', email='test@test.com', password='password')
        WarGameFactory.create_batch(4, player=user, result=WarGame.TIE)
        self.assertEqual(user.get_ties(), 4)

    def test_get_record_display(self):
        user = Player.objects.create_user(username='test-user', email='test@test.com', password='password')
        WarGameFactory.create_batch(2, player=user, result=WarGame.WIN)
        WarGameFactory.create_batch(3, player=user, result=WarGame.LOSS)
        WarGameFactory.create_batch(4, player=user, result=WarGame.TIE)
        self.assertEqual(user.get_record_display(), "2-3-4")
