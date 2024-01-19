from random import randint
from uuid import uuid4

import factory
from django.contrib.auth import get_user_model
from factory import fuzzy, lazy_attribute

from wallet.models import Wallet, Transaction


class CustomerFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')

    class Meta:
        model = get_user_model()


class WalletFactory(factory.django.DjangoModelFactory):
    owned_by = factory.SubFactory(CustomerFactory)
    is_active = True

    class Meta:
        model = Wallet


class TransactionFactory(factory.django.DjangoModelFactory):
    created_by = factory.SubFactory(CustomerFactory)
    type = fuzzy.FuzzyChoice([x[0] for x in Transaction.TypeStatus])
    ref_id = lazy_attribute(lambda x: uuid4().hex)
    amount = lazy_attribute(lambda o: randint(0, 500_000))

    class Meta:
        model = Transaction
