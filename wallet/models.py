import uuid
from django.db import models

from customer.models import Customer

class Wallet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owned_by = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=False)
    enabled_at = models.DateTimeField(auto_now_add=True)
    balance = models.DecimalField(max_digits=24, decimal_places=2, default=0)

    def __str__(self) -> str:
        return f'{self.id} - {self.balance}'