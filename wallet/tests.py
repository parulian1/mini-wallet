from uuid import uuid4
from http import HTTPStatus

from django.test import TestCase

from utils.factories import CustomerFactory, WalletFactory, TransactionFactory
from rest_framework.test import APIClient


# Create your tests here.
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


class WalletTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_enable_wallet_success(self):
        customer = CustomerFactory(xid=uuid4().hex)
        response_init = self.client.post('/api/v1/init/', data={
            'customer_xid': customer.xid
        })
        token = response_init.json().get('data', {}).get('token')
        response = self.client.post('/api/v1/wallet/',
                                    headers={
                                        'Authorization': f'Token {token}'
                                    })
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertIsNotNone(response.json().get('data', {}).get('Wallet'))

    def test_enable_wallet_failed(self):
        customer = CustomerFactory(xid=uuid4().hex)
        WalletFactory(owned_by=customer)
        response_init = self.client.post('/api/v1/init/', data={
            'customer_xid': customer.xid
        })
        token = response_init.json().get('data', {}).get('token')
        response = self.client.post('/api/v1/wallet/',
                                    headers={
                                        'Authorization': f'Token {token}'
                                    })
        self.assertEqual(response.status_code, HTTPStatus.ALREADY_REPORTED)
        self.assertIsNotNone(response.json().get('data', {}).get('error'))

    def test_disable_wallet_success(self):
        customer = CustomerFactory(xid=uuid4().hex)
        WalletFactory(owned_by=customer)
        response_init = self.client.post('/api/v1/init/', data={
            'customer_xid': customer.xid
        })
        token = response_init.json().get('data', {}).get('token')
        response = self.client.patch('/api/v1/wallet/',
                                     {'is_disabled': 'True'},
                                     format='multipart',
                                     headers={
                                         'Authorization': f'Token {token}',
                                     })
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIsNotNone(response.json().get('data', {}).get('Wallet'))

    def test_disable_wallet_failed(self):
        customer = CustomerFactory(xid=uuid4().hex)
        WalletFactory(owned_by=customer, is_active=False)
        response_init = self.client.post('/api/v1/init/', data={
            'customer_xid': customer.xid
        })
        token = response_init.json().get('data', {}).get('token')
        response = self.client.patch('/api/v1/wallet/',
                                     {'is_disabled': 'True'},
                                     format='multipart',
                                     headers={
                                         'Authorization': f'Token {token}',
                                     })
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertIsNotNone(response.json().get('data', {}).get('error'))

    def test_get_wallet(self):
        customer = CustomerFactory(xid=uuid4().hex)
        wallet = WalletFactory(owned_by=customer)
        response_init = self.client.post('/api/v1/init/', data={
            'customer_xid': customer.xid
        })
        token = response_init.json().get('data', {}).get('token')
        success_response = self.client.get('/api/v1/wallet/',
                                           headers={
                                               'Authorization': f'Token {token}',
                                           })
        self.assertEqual(success_response.status_code, HTTPStatus.OK)
        self.assertIsNotNone(success_response.json().get('data', {}).get('Wallet'))
        wallet.is_active = False
        wallet.save()
        fail_response = self.client.get('/api/v1/wallet/',
                                        headers={
                                            'Authorization': f'Token {token}',
                                        })
        self.assertEqual(fail_response.status_code, HTTPStatus.NOT_FOUND)
        self.assertIsNotNone(fail_response.json().get('data', {}).get('error'))


class TransactionTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_transactions_success(self):
        customer = CustomerFactory(xid=uuid4().hex)
        WalletFactory(owned_by=customer)
        for _ in range(10):
            TransactionFactory(created_by=customer)
        response_init = self.client.post('/api/v1/init/', data={
            'customer_xid': customer.xid
        })
        token = response_init.json().get('data', {}).get('token')
        response = self.client.get('/api/v1/wallet/transactions/',
                                   headers={
                                       'Authorization': f'Token {token}',
                                   })
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIsNotNone(response.json().get('data', {}).get('Transactions'))

    def test_get_transactions_failed(self):
        customer = CustomerFactory(xid=uuid4().hex)
        WalletFactory(owned_by=customer, is_active=False)
        for _ in range(10):
            TransactionFactory(created_by=customer)
        response_init = self.client.post('/api/v1/init/', data={
            'customer_xid': customer.xid
        })
        token = response_init.json().get('data', {}).get('token')
        response = self.client.get('/api/v1/wallet/transactions/',
                                   headers={
                                       'Authorization': f'Token {token}',
                                   })
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertIsNotNone(response.json().get('data', {}).get('error'))

    def test_transaction_deposit(self):
        customer = CustomerFactory(xid=uuid4().hex)
        WalletFactory(owned_by=customer)
        response_init = self.client.post('/api/v1/init/', data={
            'customer_xid': customer.xid
        })
        token = response_init.json().get('data', {}).get('token')
        response = self.client.post('/api/v1/wallet/deposits/',
                                    {'amount': '10000', 'reference_id': uuid4().hex},
                                    format='multipart',
                                    headers={
                                        'Authorization': f'Token {token}',
                                    })
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertIsNotNone(response.json().get('data', {}).get('deposit'))

    def test_transaction_deposit_fail(self):
        customer = CustomerFactory(xid=uuid4().hex)
        wallet = WalletFactory(owned_by=customer)
        response_init = self.client.post('/api/v1/init/', data={
            'customer_xid': customer.xid
        })
        token = response_init.json().get('data', {}).get('token')
        fail_response1 = self.client.post('/api/v1/wallet/deposits/',
                                          {'amount': '10000', 'reference_id': 'aabc'},
                                          format='multipart',
                                          headers={
                                              'Authorization': f'Token {token}',
                                          })
        self.assertEqual(fail_response1.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIsNotNone(fail_response1.json().get('data', {}).get('error'))

        wallet.is_active = False
        wallet.save()
        fail_response2 = self.client.post('/api/v1/wallet/deposits/',
                                          {'amount': '10000', 'reference_id': uuid4().hex},
                                          format='multipart',
                                          headers={
                                              'Authorization': f'Token {token}',
                                          })
        self.assertEqual(fail_response2.status_code, HTTPStatus.NOT_FOUND)
        self.assertIsNotNone(fail_response2.json().get('data', {}).get('error'))

    def test_transaction_withdraw(self):
        customer = CustomerFactory(xid=uuid4().hex)
        WalletFactory(owned_by=customer, balance=20000)
        response_init = self.client.post('/api/v1/init/', data={
            'customer_xid': customer.xid
        })
        token = response_init.json().get('data', {}).get('token')
        response = self.client.post('/api/v1/wallet/withdrawals/',
                                    {'amount': '10000', 'reference_id': uuid4().hex},
                                    format='multipart',
                                    headers={
                                        'Authorization': f'Token {token}',
                                    })
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertIsNotNone(response.json().get('data', {}).get('withdrawal'))

    def test_transaction_withdraw_fail(self):
        customer = CustomerFactory(xid=uuid4().hex)
        wallet = WalletFactory(owned_by=customer, balance=20000)
        response_init = self.client.post('/api/v1/init/', data={
            'customer_xid': customer.xid
        })
        token = response_init.json().get('data', {}).get('token')
        inv_req_response = self.client.post('/api/v1/wallet/withdrawals/',
                                            {'amount': '10000', 'reference_id': 'aac'},
                                            format='multipart',
                                            headers={
                                                'Authorization': f'Token {token}',
                                            })
        self.assertEqual(inv_req_response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIsNotNone(inv_req_response.json().get('data', {}).get('error'))

        wallet.is_active = False
        wallet.save()
        inv_wallet_req_response = self.client.post('/api/v1/wallet/withdrawals/',
                                                   {'amount': '10000', 'reference_id': uuid4().hex},
                                                   format='multipart',
                                                   headers={
                                                       'Authorization': f'Token {token}',
                                                   })
        self.assertEqual(inv_wallet_req_response.status_code, HTTPStatus.NOT_FOUND)
        self.assertIsNotNone(inv_wallet_req_response.json().get('data', {}).get('error'))
