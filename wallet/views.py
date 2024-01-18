from datetime import datetime

from customer.models import Customer
from utils.constant import ResponseCode

from utils.formatter import ApiMixin as resp
from wallet.models import Wallet
from wallet.serializers import WalletInitSerializer, WalletSerializer

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

@api_view(['POST', 'GET', 'PATCH'])
def api_wallet(request):
    print(request.user)
    user, token = JWTAuthentication().authenticate(request)
    print(user)
    wallet = Wallet.objects.filter(owned_by=user).first()
    resp_code = ResponseCode.ok
    data = {}
    if request.method == 'POST':
        if not wallet:
            wallet = Wallet.objects.create(owned_by=user)

        if wallet and wallet.is_active:
            return resp.api_response(ResponseCode.error_wallet_disabled, data={
                'error': 'wallet already active'
            })
        wallet.is_active = True
        wallet.enabled_at = datetime.now()
        wallet.save()
    return resp.api_response(resp_code, data=data)  


class WalletView(APIView):
    def post(self, request, *args, **kwargs):
        wallet = Wallet.objects.filter(owned_by=request.user).first()
        resp_code = ResponseCode.created
        data = {}
        if not wallet:
            wallet = Wallet.objects.create(owned_by=request.user)

        if wallet and wallet.is_active:
            resp_code = ResponseCode.error_wallet_disabled
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

        
