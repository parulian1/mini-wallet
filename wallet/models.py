import uuid
from django.db import models

from customer.models import Customer

class Wallet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owned_by = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=False)
    enabled_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    balance = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f'{self.id} - {self.balance}'
    

class Transaction(models.Model):
    class TypeStatus(models.TextChoices):
        deposit = 'deposit', 'Deposit'
        withdraw = 'withdraw', 'Withdraw'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    type = models.CharField(choices=TypeStatus.choices, max_length=20, default=TypeStatus.deposit)
    ref_id = models.CharField(max_length=35)
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField(default=0)