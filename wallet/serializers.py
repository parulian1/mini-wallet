from rest_framework import serializers, status


from customer.models import Customer
from utils.validator import ValidationError
from wallet.models import Wallet, Transaction


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

class WalletPatchSerializer(serializers.Serializer):
    is_disabled = serializers.BooleanField()


class WalletTransactionSerializer(serializers.Serializer):
    created_by = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    reference_id = serializers.SerializerMethodField()

    def get_created_by(self, obj):
        return obj.created_by_id.hex

    def get_status(self, obj):
        return 'success'

    def get_created_at(self, obj):
        return obj.created_at.isoformat()

    def get_reference_id(self, obj):
        return obj.ref_id

    class Meta:
        model = Transaction
        fields = (
            'id',
            'created_by',
            'type',
            'status',
            'reference_id',
            'created_at',
            'amount'
        )


class WalletTransactionDepositSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    reference_id = serializers.UUIDField()

        