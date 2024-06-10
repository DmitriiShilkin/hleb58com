from django.core.validators import (
    MinLengthValidator, MinValueValidator, MaxValueValidator
)
from django.db import models


# Модель для Промокода
class Coupon(models.Model):
    name = models.CharField(
        verbose_name='Промокод',
        unique=True,
        max_length=20,
        validators=[
            MinLengthValidator(3),
        ]
    )
    valid_from = models.DateField(
        verbose_name='Действует с',

    )
    valid_to = models.DateField(
        verbose_name='Действует до'
    )
    discount = models.IntegerField(
        verbose_name='Размер скидки, %',
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )
    is_active = models.BooleanField(
        verbose_name='Активный',
        default=False
    )

    def __str__(self):
        return self.name
