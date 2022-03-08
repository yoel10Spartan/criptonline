from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, 
    AbstractBaseUser, 
    PermissionsMixin,
)

class UserManager(BaseUserManager):
    def _create_user(self, phone_number, name, last_name, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            phone_number = phone_number,
            name = name,
            last_name = last_name,
            is_staff = is_staff,
            is_superuser = is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, name,last_name, password=None, **extra_fields):
        return self._create_user(phone_number, name, last_name, password, False, False, **extra_fields)

    def create_superuser(self, phone_number, name, last_name, password=None, **extra_fields):
        return self._create_user(phone_number, name, last_name, password,  True, True, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField('name', max_length = 255)
    last_name = models.CharField('last_name', max_length = 255)
    phone_number = models.BigIntegerField('phone_number', unique=True)

    last_login = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name', 'last_name']

    def __str__(self):
        return '{} {}'.format(self.name, self.last_name)