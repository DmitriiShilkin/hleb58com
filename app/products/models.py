from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from .constants import PROMOCODE_PERCENT, STICKERS
from .services import get_image_path


# Модель для Категории
class Category(models.Model):
    created_at = models.DateTimeField(
        default=timezone.now,
        editable=False
    )
    modified_at = models.DateTimeField(
        editable=False,
        blank=True,
        null=True
    )
    name = models.CharField(
        verbose_name='Название',
        unique=True,
        max_length=254,
        validators=[
            MinLengthValidator(5),
        ]
    )
    description = models.CharField(
        verbose_name='Описание',
        blank=True,
        null=True,
        max_length=254
    )

    def __str__(self):
        return self.name


# Модель для Промокода
class PromoCode(models.Model):
    created_at = models.DateTimeField(
        default=timezone.now,
        editable=False
    )
    name = models.CharField(
        verbose_name='Название',
        unique=True,
        max_length=10,
        validators=[
            MinLengthValidator(3),
        ]
    )
    discount = models.FloatField(
        verbose_name='Размер скидки',
        validators=[
            MinValueValidator(0.0),
        ]
    )
    expire_at = models.DateTimeField(
        verbose_name='Действует до',
    )
    is_percent = models.BooleanField(
        verbose_name='Процент',
        choices=PROMOCODE_PERCENT,
        default=True
    )

    def __str__(self):
        return self.name

    def is_expired(self):
        if self.expire_at <= timezone.now():
            return True
        else:
            return False


# Модель для Продукта
class Product(models.Model):
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
    name = models.CharField(
        verbose_name='Название',
        unique=True,
        max_length=254,
        validators=[
            MinLengthValidator(5),
        ]
    )
    description = models.TextField(
        verbose_name='Описание',
        validators=[
            MinLengthValidator(5),
        ]
    )
    weight = models.IntegerField(
        verbose_name='Вес, г.',
        validators=[
            MinValueValidator(0),
        ]
    )
    price = models.FloatField(
        verbose_name='Базовая цена, руб.',
        validators=[
            MinValueValidator(0.0),
        ]
    )
    new_price = models.FloatField(
        verbose_name='Цена с учетом скидки/надбавки, руб.',
        editable=False,
        default=price
    )
    discount = models.FloatField(
        verbose_name='Скидка, %',
        default=0.0,
        validators=[
            MinValueValidator(0.0),
        ]
    )
    discount_rub = models.FloatField(
        verbose_name='Скидка, руб.',
        default=0.0,
        validators=[
            MinValueValidator(0.0),
        ]
    )
    increment = models.FloatField(
        verbose_name='Надбавка в процентах',
        default=0.0,
        validators=[
            MinValueValidator(0.0),
        ]
    )
    increment_rub = models.FloatField(
        verbose_name='Надбавка в рублях',
        default=0.0,
        validators=[
            MinValueValidator(0.0),
        ]
    )
    quantity = models.IntegerField(
        verbose_name='Количество, шт.',
        validators=[
            MinValueValidator(0),
        ],
        default=0
    )
    is_visible = models.BooleanField(
        verbose_name='Видимость',
        default=True
    )
    sticker = models.CharField(
        verbose_name='Наклейка',
        max_length=3,
        choices=STICKERS,
        default='NEW'
    )
    category = models.ManyToManyField(
        Category,
        verbose_name='Категория',
        related_name='products'
    )
    promo_code = models.ManyToManyField(
        PromoCode,
        verbose_name='Промокод',
        related_name='products',
        blank=True,
    )

    def __str__(self):
        return self.name

    def make_visible(self):
        self.is_visible = True
        self.save()

    def make_invisible(self):
        self.is_visible = False
        self.save()

    def save(self, *args, **kwargs):
        self.new_price = self.price * (1 - self.discount / 100 + self.increment / 100) \
                         - self.discount_rub + self.increment_rub
        if self.new_price < 0:
            self.new_price = 0

        super().save(*args, **kwargs)


# Модель для Изображений Продукта
class ProductImage(models.Model):
    created_at = models.DateTimeField(
        verbose_name='Создан',
        default=timezone.now,
        editable=False
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to=get_image_path,
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.pk}: {self.image}'

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
