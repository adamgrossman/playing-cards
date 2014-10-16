import user
from django.core import mail
from django.test import TestCase
from cards.forms import EmailUserCreationForm
from cards.models import Card, Player, WarGame
from cards.test_utils import run_pyflakes_for_package, run_pep8_for_package
from cards.utils import create_deck


def my_max(number_one, number_two):
    if number_one >= number_two:
        return number_one
    else:
        return number_two


# class BasicMathTestCase(TestCase):
#     def test_my_max(self):
#         self.assertEqual(my_max(5, 3), 5)
#         self.assertEqual(my_max(3, 5), 5)
#         self.assertEqual(my_max(5, 5), 5)
#
#     # def test_my_max_fail(self):
#     #     self.assertEqual(my_max(3, 5), 3)
#
#     def test_math(self):
#         a = 1
#         b = 2
#         self.assertEqual(a + b, 3)

    # def test_failing_case(self):
    #     a = 1
    #     b = 1
    #     self.assertEqual(a + b, 1)


class UtilTest(TestCase):
    def test_create_deck(self):
        self.assertEqual(Card.objects.count(), 0)
        create_deck()
        self.assertEqual(len(Card.objects.all()), 52)


class ModelTestCase(TestCase):
    def test_get_ranking(self):
        """Test that we get the proper ranking for a card"""
        card = Card.objects.create(suit=Card.CLUB, rank="jack")
        self.assertEqual(card.get_ranking(), 11)


class PlayerModelTest(TestCase):
    def create_war_game(self, user, result=WarGame.LOSS):
        WarGame.objects.create(result=result, player=user)

    def test_get_wins(self):
        user = Player.objects.create_user(username='test-user', email='test@test.com', password='password')
        self.create_war_game(user, WarGame.WIN)
        self.create_war_game(user, WarGame.WIN)
        self.assertEqual(user.get_wins(), 2)

    def test_get_losses(self):
        user = Player.objects.create_user(username='test-user', email='test@test.com', password='password')
        self.create_war_game(user, WarGame.LOSS)
        self.create_war_game(user, WarGame.LOSS)
        self.create_war_game(user, WarGame.LOSS)
        self.assertEqual(user.get_losses(), 3)


class get_war_result(TestCase):
    def setUp(self):
        self.card_one = Card.objects.create(suit=Card.CLUB, rank="three")
        self.card_two = Card.objects.create(suit=Card.CLUB, rank="two")
        self.card_three = Card.objects.create(suit=Card.CLUB, rank="three")

    def test_get_war_result(self):
        self.assertEqual(self.card_one.get_war_result(self.card_two), 1)
        self.assertEqual(self.card_one.get_war_result(self.card_three), 0)
        self.assertEqual(self.card_two.get_war_result(self.card_three), -1)


class FormTestCase(TestCase):
    def test_clean_username_pass(self):
        Player.objects.create_user(username='test-user')

        form = EmailUserCreationForm()
        form.cleaned_data = {'username': 'test'}

        self.assertEqual(form.clean_username(), 'test')

    def test_register_sends_email(self):
        form = EmailUserCreationForm()
        form.cleaned_data = {
            'username': 'test',
            'email': 'test@test.com',
            'password1': 'test-pw',
            'password2': 'test-pw',
        }
        form.save()
        # Check there is an email to send
        self.assertEqual(len(mail.outbox), 1)
        # Check the subject is what we expect
        self.assertEqual(mail.outbox[0].subject, 'Welcome!')


# class SyntaxTest(TestCase):
#     def test_syntax(self):
#         """
#         Run pyflakes/pep8 across the code base to check for potential errors.
#         """
#         packages = ['cards']
#         warnings = []
#         # Eventually should use flake8 instead so we can ignore specific lines via a comment
#         for package in packages:
#             warnings.extend(run_pyflakes_for_package(package, extra_ignore=("_settings",)))
#             warnings.extend(run_pep8_for_package(package, extra_ignore=("_settings",)))
#         if warnings:
#             self.fail("{0} Syntax warnings!\n\n{1}".format(len(warnings), "\n".join(warnings)))
