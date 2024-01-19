from datetime import datetime

from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, FormParser

from customer.models import Customer
from utils.constant import ResponseCode

from utils.formatter import ApiMixin as resp
from wallet.models import Wallet, Transaction
from wallet.serializers import WalletInitSerializer, WalletSerializer, WalletPatchSerializer, \
    WalletTransactionSerializer, WalletTransactionDepositSerializer

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication


# Create your views here.
@api_view(['POST', ])
def api_init(request):
    serializer = WalletInitSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    exist_user = Customer.objects.get(xid=serializer.data.get('customer_xid').strip())
    return resp.api_response(ResponseCode.ok, data={
        'token': exist_user.access_token().get('access')
    })


class WalletView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        wallet = Wallet.objects.filter(owned_by=request.user).first()
        resp_code = ResponseCode.created
        if not wallet:
            wallet = Wallet.objects.create(owned_by=request.user)

        if wallet and wallet.is_active:
            resp_code = ResponseCode.error_wallet_already_enabled
            data = {
                'error': 'wallet already active'
            }
            return resp.api_response(resp_code, data=data)
        wallet.is_active = True
        wallet.enabled_at = datetime.now()
        wallet.save()
        wallet_serializer = WalletSerializer(wallet)
        data = {
            'Wallet': wallet_serializer.data
        }
        return resp.api_response(resp_code, data=data)

    def get_object(self, request):
        return Wallet.objects.filter(owned_by=request.user).first()

    def patch(self, request, *args, **kwargs):
        # Custom logic for handling PATCH request
        serializer = WalletPatchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        resp_code = ResponseCode.ok
        wallet = self.get_object(request=request)
        is_disabled = data.get('is_disabled')
        # is_disabled = True if is_disabled_req in [True, 'true', 'TRUE', 'True'] else False

        if is_disabled:
            if not wallet.is_active:
                resp_code = ResponseCode.error_wallet_already_disabled
                data = {
                    'error': 'wallet already active'
                }
            else:
                wallet.is_active = False
                wallet.save()
                wallet_serializer = WalletSerializer(wallet)
                data = {
                    'Wallet': wallet_serializer.data
                }
        else:
            resp_code = ResponseCode.error_forbidden
            data = {
                'error': 'This method does not allowed for enable wallet'
            }
        return resp.api_response(resp_code, data=data)

    def get(self, request, *args, **kwargs):
        resp_code = ResponseCode.ok
        wallet = self.get_object(request=request)
        if wallet.is_active:
            serializer = WalletSerializer(wallet)
            data = {
                'Wallet': serializer.data
            }
        else:
            resp_code = ResponseCode.error_wallet_is_disabled
            data = {
                'error': 'Wallet disabled'
            }
        return resp.api_response(resp_code, data=data)


class WalletTransactionView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self, request):
        return Wallet.objects.filter(owned_by=request.user).first()

    def get_wallet_transactions(self, user):
        return Transaction.objects.filter(created_by=user)

    def get(self, request, *args, **kwargs):
        resp_code = ResponseCode.ok
        wallet = self.get_object(request=request)
        if wallet.is_active:
            transaction_serializer = WalletTransactionSerializer(self.get_wallet_transactions(user=request.user),
                                                                 many=True)
            data = {
                'Transactions': transaction_serializer.data
            }

        else:
            resp_code = ResponseCode.error_wallet_is_disabled
            data = {
                'error': 'Wallet disabled'
            }
        return resp.api_response(resp_code, data=data)


class WalletTransactionDepositView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self, request):
        return Wallet.objects.filter(owned_by=request.user).first()

    def post(self, request, *args, **kwargs):
        wallet = self.get_object(request=request)
        if not wallet or wallet.is_active is False:
            return resp.api_response(ResponseCode.error_wallet_is_disabled, data={
                'error': 'Wallet is disabled'
            })

        serializer = WalletTransactionDepositSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return resp.api_response(ResponseCode.error_param, data={
                'error': 'Invalid param value(s)'
            })
        data = serializer.validated_data
        transaction = Transaction.objects.create(created_by=request.user, amount=data.get('amount'),
                                                 ref_id=data.get('reference_id').hex,
                                                 type=Transaction.TypeStatus.deposit)
        wallet.balance += transaction.amount
        wallet.save()
        return resp.api_response(ResponseCode.created, data={
            'deposit': WalletTransactionSerializer(transaction).data
        })


class WalletTransactionWithdrawView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self, request):
        return Wallet.objects.filter(owned_by=request.user).first()

    def post(self, request, *args, **kwargs):
        wallet = self.get_object(request=request)
        if not wallet or wallet.is_active is False:
            return resp.api_response(ResponseCode.error_wallet_is_disabled, data={
                'error': 'Wallet is disabled'
            })

        serializer = WalletTransactionDepositSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return resp.api_response(ResponseCode.error_param, data={
                'error': 'Invalid param value(s)'
            })
        data = serializer.validated_data
        amount = data.get('amount')
        if wallet.balance >= amount:
            transaction = Transaction.objects.create(created_by=request.user, amount=amount,
                                                     ref_id=data.get('reference_id').hex,
                                                     type=Transaction.TypeStatus.withdraw)
            wallet.balance -= amount
            wallet.save()
            return resp.api_response(ResponseCode.created, data={
                'withdrawal': WalletTransactionSerializer(transaction).data
            })
        else:
            return resp.api_response(ResponseCode.error_wallet_insufficient_balance, data={
                'error': 'Insufficient wallet balance'
            })
