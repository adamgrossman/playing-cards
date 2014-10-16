import factory


class WarGameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'cards.WarGame'
