from datetime import datetime

from rest_framework.parsers import MultiPartParser, FormParser

from customer.models import Customer
from utils.constant import ResponseCode

from utils.formatter import ApiMixin as resp
from wallet.models import Wallet
from wallet.serializers import WalletInitSerializer, WalletSerializer, WalletPatchSerializer

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
        wallet = self.get_object(request=self.request)
        is_disabled_req = data.get('is_disabled')
        is_disabled = True if is_disabled_req in [True, 'true', 'TRUE', 'True'] else False

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
        wallet = self.get_object(request=self.request)
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
