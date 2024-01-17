import uuid
from django.db import models

from customer.models import Customer

class Transaction(models.Model):
    class TypeStatus(models.TextChoices):
        deposit = 'deposit', 'Deposit'
        withdraw = 'withdraw', 'Withdraw'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    type = models.CharField(choices=TypeStatus.choices, max_length=20, default=TypeStatus.deposit)
    ref_id = models.CharField(max_length=25)
