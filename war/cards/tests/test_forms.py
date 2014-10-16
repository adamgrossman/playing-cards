from django.core import mail
from django.core.exceptions import ValidationError
from django.test import TestCase
from cards.forms import EmailUserCreationForm
from cards.models import Player


class FormTestCase(TestCase):
    def test_clean_username_exception(self):
        # Create a player so that this username we're testing is already taken
        Player.objects.create_user(username='test-user')

        # set up the form for testing
        form = EmailUserCreationForm()
        form.cleaned_data = {'username': 'test-user'}

        # use a context manager to watch for the validation error being raised
        with self.assertRaises(ValidationError):
            form.clean_username()

    def test_clean_username(self):
        # set up the form for testing
        form = EmailUserCreationForm()
        form.cleaned_data = {'username': 'test-user'}
        self.assertEquals(form.clean_username(), 'test-user')

    def test_register_sends_email(self):
        form = EmailUserCreationForm()
        form.cleaned_data = {
            'username': 'test',
            'email': 'test@test.com',
            'password1': 'test-pw',
            'password2': 'test-pw',
        }
        form.save()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Welcome!')
