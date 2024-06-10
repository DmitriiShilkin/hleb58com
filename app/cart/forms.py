from django import forms

from .constants import PRODUCT_QUANTITY_CHOICES


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES, coerce=int, label='Количество'
    )
    update = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput
    )
