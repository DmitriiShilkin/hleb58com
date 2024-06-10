import uuid
from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone

from .constants import STATUSES
from products.models import Product
from sign.models import CustomUser
from coupons.models import Coupon


# Модель для Заказа
class Order(models.Model):
    uid = models.UUIDField(
        verbose_name='Уникальный идентификатор',
        default=uuid.uuid4,
        editable=False
    )
    created_at = models.DateTimeField(
        verbose_name='Создан',
        default=timezone.now,
        editable=False
    )
    modified_at = models.DateTimeField(
        verbose_name='Изменен',
        editable=False,
        blank=True,
        null=True
    )
    ready_at = models.DateTimeField(
        verbose_name='Дата и время готовности',
        editable=False,
        blank=True,
        null=True
    )
    wish_date_at = models.DateField(
        verbose_name='На какую дату',
    )
    is_complete = models.BooleanField(
        verbose_name='Завершен',
        default=False
    )
    status = models.CharField(
        verbose_name='Статус',
        max_length=3,
        choices=STATUSES,
        default='NEW'
    )
    discount = models.IntegerField(
        verbose_name='Скидка',
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )
    is_paid = models.BooleanField(
        verbose_name='Оплачен',
        default=False
    )
    customer = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )
    coupon = models.ForeignKey(
        Coupon,
        related_name='orders',
        null=True,
        blank=True,
        on_delete=models.SET(None)
    )

    # функция reverse позволяет нам указывать не путь вида /order/…, а название пути, которое мы задали
    # в файле urls.py для аргумента name
    def get_absolute_url(self):
        return reverse('order_detail', args=[str(self.pk)])

    # возвращает время завершения заказа
    def finish_order(self):
        self.ready_at = timezone.now()
        self.is_complete = True
        self.save()

    # возвращает время выполнения заказа в часах-минутах
    def get_duration(self):
        if self.is_complete:
            delta = (self.ready_at - self.created_at)
        else:
            delta = timezone.now() - self.created_at
        hours, minutes = str(delta)[:-10].split(':')
        return f'{hours} часов {minutes} минут'

    # отменяет заказ
    def set_canceled(self):
        if self.status not in ['CAN', 'FIN']:
            self.status = 'CAN'
            self.save()
        else:
            raise ValueError(
                "Заказ не может быть отменен - он либо уже отменен, либо завершен!"
            )

    def __str__(self):
        return f'Заказ {self.uid}'

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal('100'))

    def get_discount(self):
        if self.discount:
            return (self.discount / Decimal('100')) * (self.get_total_cost() / (1 - self.discount / Decimal('100')))
        return Decimal('0')


# Модель для товара из заказа
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='order_items'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    amount = models.PositiveIntegerField(
        default=1
    )

    def __str__(self):
        return f'{self.product.name}'

    def get_cost(self):
        return self.price * self.amount
