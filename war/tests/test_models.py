from django.test import TestCase
from cards.models import Card, Player, WarGame
from tests.factories import WarGameFactory, PlayerFactory


class ModelTestCase(TestCase):
    def setUp(self):
        PlayerFactory.create_batch(3)

    # def test_failing_case(self):
    #     a = 2
    #     b = 3
    #     self.assertEqual(a * b, 6)

    def test_get_ranking(self):
        """Test that we get the proper ranking for a card"""
        card = Card.objects.create(suit=Card.CLUB, rank="jack")
        self.assertEqual(card.get_ranking(), 11)

    def create_war_game(self, user, result=WarGame.LOSS):
        WarGame.objects.create(result=result, player=user)

    def test_get_wins(self):
        # user = Player.objects.create_user(username='test-user', email='test@test.com', password='password')
        user = PlayerFactory(email='test@test.com', password='password')
        WarGameFactory.create_batch(2, player=user, result=WarGame.WIN)
        # self.create_war_game(user, WarGame.WIN)
        # self.create_war_game(user, WarGame.WIN)
        self.assertEqual(user.get_wins(), 2)

    def test_get_losses(self):
        # user = Player.objects.create_user(username='test-user', email='test@test.com', password='password')
        user = PlayerFactory(email='test@test.com', password='password')
        WarGameFactory.create_batch(3, player=user, result=WarGame.LOSS)
        # self.create_war_game(user, WarGame.LOSS)
        # self.create_war_game(user, WarGame.LOSS)
        # self.create_war_game(user, WarGame.LOSS)
        self.assertEqual(user.get_losses(), 3)

    def test_get_ties(self):
        user = PlayerFactory(email='test@test.com', password='password')
        WarGameFactory.create_batch(4, player=user, result=WarGame.TIE)
        self.assertEqual(user.get_ties(), 4)

    def test_get_record_display(self):
        # user = Player.objects.create_user(username='test-user', email='test@test.com', password='password')
        user = PlayerFactory(email='test@test.com', password='password')
        WarGameFactory.create_batch(2, player=user, result=WarGame.WIN)
        WarGameFactory.create_batch(3, player=user, result=WarGame.LOSS)
        WarGameFactory.create_batch(4, player=user, result=WarGame.TIE)
        self.assertEqual(user.get_record_display(), "2-3-4")

