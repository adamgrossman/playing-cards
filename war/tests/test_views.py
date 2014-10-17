from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.test import TestCase
from mock import patch, Mock
from cards.models import Player, WarGame
from cards.utils import create_deck, get_random_comic
from tests.factories import WarGameFactory


class ViewTestCase(TestCase):
    def setUp(self):
        create_deck()

    def create_war_game(self, user, result=WarGame.LOSS):
        # WarGame.objects.create(result=result, player=user)
        WarGameFactory(result=result, player=user)

    # @patch('cards.utils.requests')
    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertIn(b'<p>Suit: spade, Rank: two</p>', response.content)
        self.assertEqual(response.context['cards'].count(), 52)

    def test_faq_page(self):
        response = self.client.get(reverse('faq'))
        self.assertIn(b'<p>Q: Can I win real money on this website?</p>\n    <p>A: Nope, this is not real, sorry.</p>', response.content)

    def test_card_filters_page(self):
        response = self.client.get(reverse('filters'))
        self.assertIn(b'<p>\n            Capitalized Suit: 0 <br>\n            Uppercased Rank: KING\n        </p>', response.content)
        self.assertEqual(response.context['cards'].count(), 52)

    def test_register_page(self):
        username = 'new-user'
        data = {
            'username': username,
            'email': 'test@test.com',
            'password1': 'test',
            'password2': 'test'
        }
        response = self.client.post(reverse('register'), data)

        # Check this user was created in the database
        self.assertTrue(Player.objects.filter(username=username).exists())

        # Check it's a redirect to the profile page
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertTrue(response.get('location').endswith(reverse('profile')))

    def login_page(self):
        username = 'new-user'
        data = {
            'username': username,
            'password': 'password'
        }
        response = self.client.post(reverse('login'), data)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertTrue(response.get('location').endswith(reverse('profile')))

    def test_profile_page(self):
        # Create user and log them in
        password = 'passsword'
        user = Player.objects.create_user(username='test-user', email='test@test.com', password=password)
        self.client.login(username=user.username, password=password)

        # Set up some war game entries
        self.create_war_game(user)
        self.create_war_game(user, WarGame.WIN)

        # Make the url call and check the html and games queryset length
        response = self.client.get(reverse('profile'))
        self.assertInHTML('<p>Your email address is {}</p>'.format(user.email), response.content)
        self.assertEqual(len(response.context['games']), 2)

    @patch('cards.utils.requests')
    def test_xkcd_page(self, mock_requests):
        mock_comic = {
            'num': 1433,
            'year': "2014",
            'safe_title': "Lightsaber",
            'alt': "A long time in the future, in a galaxy far, far, away.",
            'transcript': "An unusual gamma-ray burst originating from somewhere across the universe.",
            'img': "http://imgs.xkcd.com/comics/lightsaber.png",
            'title': "Lightsaber",
        }
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_comic
        mock_requests.get.return_value = mock_response
        self.assertEqual(get_random_comic()['num'], 1433)