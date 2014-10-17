import factory
from cards.models import Player


class WarGameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'cards.WarGame'


class PlayerFactory(factory.DjangoModelFactory):
    class Meta:
        model = Player
    username = factory.Sequence(lambda i: 'User%d' % i)