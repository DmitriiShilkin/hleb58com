from django import forms

from .models import Coupon


# Форма для промокода
class CouponForm(forms.ModelForm):

    valid_from = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
        }, format='%Y-%m-%d'),
        label="Действует c"
    )
    valid_to = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
        }, format='%Y-%m-%d'),
        label="Действует до"
    )

    class Meta:
        model = Coupon
        fields = [
            'name',
            'valid_from',
            'valid_to',
            'discount',
            'is_active',
        ]


# форма для применения промокода
class CouponApplyForm(forms.Form):
    name = forms.CharField(
        label='Промокод',
        min_length=3,
        max_length=20
    )
