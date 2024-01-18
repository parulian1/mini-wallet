from rest_framework import serializers, status


from customer.models import Customer
from utils.validator import ValidationError
from wallet.models import Wallet

class WalletInitSerializer(serializers.Serializer):
    customer_xid = serializers.CharField(required=True, max_length=35)

    def validate(self, attrs):
        exist_user = Customer.objects.filter(xid=attrs.get('customer_xid',  None)).first()
        if not exist_user:
            error = ValidationError({
                'status': 'fail', 
                'data': {
                    'error': 'User does not exists'
                }})
            error.status_code = status.HTTP_404_NOT_FOUND
            raise error
        return attrs
    

class WalletSerializer(serializers.Serializer):
    owned_by = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    enabled_at = serializers.SerializerMethodField()

    def get_owned_by(self, obj):
        return obj.owned_by_id.hex
    
    def get_status(self, obj):
        return 'enabled' if obj.is_active else 'disabled'
    
    def get_enabled_at(self, obj):
        return obj.enabled_at.isoformat()
    
    class Meta:
        model = Wallet
        fields = (
            'id',
            'owned_by',
            'status',
            'enabled_at',
            'balance',
        )

        