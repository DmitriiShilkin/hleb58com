from django.db import models

from .constants import STAFF
from sign.models import CustomUser


# Модель для Персонала
class Staff(CustomUser):
    position = models.CharField(
        verbose_name='Должность',
        max_length=3,
        choices=STAFF,
        default='MNR'
    )
    contract = models.CharField(
        verbose_name='Номер трудового договора',
        max_length=32,
        unique=True
    )

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"

    def make_active(self):
        self.is_active = True
        self.save()

    def make_inactive(self):
        self.is_active = False
        self.save()
