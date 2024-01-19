# yourapp/models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import uuid

from rest_framework_simplejwt.tokens import RefreshToken


class CustomUserManager(BaseUserManager):
    def create_user(self, **extra_fields):
        user = self.model(**extra_fields)
        user.save(using=self._db)
        return user

    def create_superuser(self, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(**extra_fields)


class Customer(AbstractBaseUser, PermissionsMixin):
    xid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = CustomUserManager()
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'xid'
    USER_ID_FIELD = 'xid'

    def __str__(self):
        return self.xid.hex

    def full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def tokenize(self):
        """
            info inside bearer token of users, expired 1 days default, if you want to create forever token,
            just change expired days to 100 years (in days) LOL
        """

        token = RefreshToken.for_user(self)

        return token

    def access_token(self):
        """ generate for access token when register and refresh token """

        tokenize = self.tokenize()
        return {
            'refresh': str(tokenize),
            'access': str(tokenize.access_token),
            'full_name': self.full_name()
        }
