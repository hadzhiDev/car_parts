from django.contrib.auth.models import Permission, Group
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

from phonenumber_field.modelfields import PhoneNumberField

from .managers import UserManager


class User(AbstractUser):
    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ('-date_joined',)

    ROLES = (
        ('admin', 'Администратор'),
        ('controller', 'Контролер'),
    )

    username = None
    email = models.EmailField(verbose_name='электронная почта', unique=True, blank=False, null=False)
    phone = PhoneNumberField(max_length=100, unique=True, verbose_name='номер телефона', blank=True, null=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{str(self.email) or self.first_name}'