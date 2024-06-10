# Generated by Django 5.0.1 on 2024-06-09 14:26

import django.core.validators
import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('coupons', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('amount', models.PositiveIntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='Уникальный идентификатор')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Создан')),
                ('modified_at', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='Изменен')),
                ('ready_at', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='Дата и время готовности')),
                ('wish_date_at', models.DateField(verbose_name='На какую дату')),
                ('is_complete', models.BooleanField(default=False, verbose_name='Завершен')),
                ('status', models.CharField(choices=[('NEW', 'Новый'), ('CCK', 'Готовится'), ('ASM', 'На сборке'), ('DLV', 'Передан в доставку'), ('FIN', 'Завершен'), ('CAN', 'Отменен')], default='NEW', max_length=3, verbose_name='Статус')),
                ('discount', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Скидка')),
                ('is_paid', models.BooleanField(default=False, verbose_name='Оплачен')),
                ('coupon', models.ForeignKey(blank=True, null=True, on_delete=models.SET(None), related_name='orders', to='coupons.coupon')),
            ],
        ),
    ]
