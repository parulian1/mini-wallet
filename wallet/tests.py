import factory

from uuid import uuid4
from http import HTTPStatus

from django.test import TestCase
from django.contrib.auth import get_user_model

from wallet.models import Wallet


# Create your tests here.
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


class InitApiTests(TestCase):
    def setUp(self):
        pass

    def test_init_failed(self):
        response = self.client.post('/api/v1/init/', data={
            'customer_xid': str(uuid4().hex)
        })
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response.json().get('status'), 'fail')

    def test_init_success(self):
        customer = CustomerFactory(xid=uuid4().hex)
        response = self.client.post('/api/v1/init/', data={
            'customer_xid': customer.xid
        })
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json().get('status'), 'success')
        self.assertIsNotNone(response.json().get('data', {}).get('token'))

    def test_enable_wallet_success(self):
        customer = CustomerFactory(xid=uuid4().hex)
        response_init = self.client.post('/api/v1/init/', data={
            'customer_xid': customer.xid
        })
        token = response_init.json().get('data', {}).get('token')
        response = self.client.post('/api/v1/wallet/', headers={
                    'Authorization': f'Token {token}'
                })
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertIsNotNone(response.json().get('data', {}).get('Wallet'))

    def test_enable_wallet_failed(self):
        customer = CustomerFactory(xid=uuid4().hex)
        wallet = WalletFactory(owned_by=customer)
        response_init = self.client.post('/api/v1/init/', data={
            'customer_xid': customer.xid
        })
        token = response_init.json().get('data', {}).get('token')
        response = self.client.post('/api/v1/wallet/', headers={
                    'Authorization': f'Token {token}'
                })
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertIsNotNone(response.json().get('data', {}).get('error'))

