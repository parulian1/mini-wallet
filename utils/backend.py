# yourapp/auth_backends.py
from customer.models import Customer

class IdAuthenticationBackend:
    def authenticate(self, request, id=None):
        self.get_user(user_id=id)

    def get_user(self, user_id):
        try:
            return Customer.objects.get(pk=user_id)
        except Customer.DoesNotExist:
            return None
