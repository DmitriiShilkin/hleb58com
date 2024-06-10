from django import forms
from django.core.exceptions import ValidationError
from django.forms import DateInput
from django.utils import timezone

from .constants import STATUSES
from .models import Order


# Форма для создания заказа
class OrderCreateForm(forms.ModelForm):
    wish_date_at = forms.DateField(
        widget=DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        label='На какую дату',
    )

    class Meta:
        model = Order
        fields = [
            'wish_date_at',
        ]

    def clean(self):
        cleaned_data = super().clean()
        wish_date_at = cleaned_data.get("wish_date_at")
        if wish_date_at < timezone.now().date():
            raise ValidationError(
                "Выбранная дата не может быть раньше текущей!"
            )
        return cleaned_data


class OrderUpdateForm(forms.ModelForm):
    wish_date_at = forms.DateField(
        widget=DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        label='На какую дату',
    )

    class Meta:
        model = Order
        fields = [
            'wish_date_at',
        ]

    def clean(self):
        order_db = self.instance
        cleaned_data = super().clean()
        wish_date_at = cleaned_data.get("wish_date_at")
        if order_db.status in ['CAN', 'FIN']:
            raise ValidationError(
                f'Текущий статус заказа "{order_db.get_status_display()}" и '
                f'он не может быть изменен"!'
            )
        if wish_date_at < timezone.now().date():
            raise ValidationError(
                "Выбранная дата не может быть раньше текущей!"
            )
        return cleaned_data


class OrderUpdateByStaffForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = [
            'status',
        ]

    def clean(self):
        order_db = self.instance
        cleaned_data = super().clean()
        status = cleaned_data.get("status")
        if (
                (status == 'NEW' and order_db.status in ['CCK', 'ASM', 'DLV', 'FIN', 'CAN']) or
                (status == 'CCK' and order_db.status in ['ASM', 'DLV', 'FIN', 'CAN']) or
                (status == 'ASM' and order_db.status in ['DLV', 'FIN', 'CAN']) or
                (status == 'DLV' and order_db.status in ['FIN', 'CAN']) or
                (status == 'FIN' and order_db.status == 'CAN') or
                (status == 'CAN' and order_db.status == 'FIN')
        ):
            status = dict(STATUSES).get(status)
            raise ValidationError(
                f'Текущий статус "{order_db.get_status_display()}" и '
                f'не может быть изменен на "{status}"!'
            )
        return cleaned_data


class OrderRepeatForm(forms.ModelForm):
    wish_date_at = forms.DateField(
        widget=DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        label='На какую дату',
    )

    class Meta:
        model = Order
        fields = [
            'wish_date_at',
        ]

    def clean(self):
        cleaned_data = super().clean()
        wish_date_at = cleaned_data.get("wish_date_at")
        if wish_date_at < timezone.now().date():
            raise ValidationError(
                "Выбранная дата не может быть раньше текущей!"
            )
        return cleaned_data
