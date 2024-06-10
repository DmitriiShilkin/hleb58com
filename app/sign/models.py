import datetime
from dateutil.relativedelta import relativedelta

import uuid

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, EmailValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

from .constants import ONE_TIME_CODE_EXPIRY_MINUTES
from company.validators import phone_number_validator


# Модель пользователя
class CustomUser(AbstractUser):
    uid = models.UUIDField(
        verbose_name='Уникальный идентификатор',
        default=uuid.uuid4,
        editable=False
    )
    username = models.CharField(
        max_length=20,
        verbose_name='Имя пользователя',
        unique=True,
        validators=[
            MinLengthValidator(2),
        ],
    )
    email = models.EmailField(
        max_length=254,
        verbose_name='Email',
        unique=True,
        validators=[
            MinLengthValidator(6),
            EmailValidator,
        ],
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=20,
        validators=[
            MinLengthValidator(2),
        ]
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=20,
        validators=[
            MinLengthValidator(2),
        ]
    )
    middle_name = models.CharField(
        verbose_name='Отчество',
        max_length=20,
        validators=[
            MinLengthValidator(2),
        ],
        blank=True,
        null=True,
    )
    individual_taxpayer_number = models.CharField(
        verbose_name='ИНН',
        max_length=12,
        validators=[
            MinLengthValidator(12),
        ],
        blank=True,
        null=True,
    )
    birthdate = models.DateField(
        verbose_name='Дата рождения',
        blank=True,
        null=True,
        validators=[
            MinValueValidator(datetime.date(1950, 1, 1)),
            MaxValueValidator(datetime.date.today()-relativedelta(years=18))
        ]
    )
    city = models.CharField(
        verbose_name='Город',
        max_length=20,
        validators=[
            MinLengthValidator(2),
        ],
        blank=True,
        null=True,
    )
    phone = models.CharField(
        verbose_name='Номер телефона: +',
        max_length=12,
        validators=[
            MinLengthValidator(11),
            phone_number_validator,
        ],
        blank=True,
        null=True,
    )
    telegram = models.CharField(
        verbose_name='Telegram',
        max_length=20,
        validators=[
            MinLengthValidator(2),
        ],
        unique=True,
        blank=True,
        null=True,
    )
    whatsapp = models.CharField(
        verbose_name='WhatsApp',
        max_length=20,
        validators=[
            MinLengthValidator(2),
        ],
        unique=True,
        blank=True,
        null=True,
    )
    viber = models.CharField(
        verbose_name='Viber',
        max_length=20,
        validators=[
            MinLengthValidator(2),
        ],
        unique=True,
        blank=True,
        null=True,
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class OneTimeCode(models.Model):
    code = models.CharField(max_length=10)
    user = models.CharField(max_length=255)
    created_at = models.DateTimeField(
        default=timezone.now,
        editable=False,
    )

    def is_expired(self):
        expires_at = self.created_at + timezone.timedelta(
            minutes=ONE_TIME_CODE_EXPIRY_MINUTES
        )
        return timezone.now() > expires_at
