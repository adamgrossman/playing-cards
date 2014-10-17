from django.core import mail
from django.test import TestCase
from cards.forms import EmailUserCreationForm
# from cards.models import Player
from tests.factories import PlayerFactory


class FormTestCase(TestCase):
    def test_clean_username_pass(self):
        # Player.objects.create_user(username='test-user')
        PlayerFactory()

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