from django import forms
from django.core.exceptions import ValidationError
from django.forms import NumberInput

from .models import Product, Category


# Форма для создания продукта
class ProductForm(forms.ModelForm):
    weight = forms.IntegerField(widget=NumberInput(
        attrs={'type': 'number', 'id': 'weight', 'oninput': 'limit_input(id, 4)'}),
        label='Вес, г.',
        min_value=0,
        max_value=9999,
        initial=0,
    )
    price = forms.FloatField(widget=NumberInput(
        attrs={'type': 'number', 'id': 'price', 'oninput': 'limit_input(id, 7)'}),
        label='Цена, руб.',
        min_value=0.0,
        max_value=9999.99,
        initial=0.0,
    )
    discount = forms.FloatField(widget=NumberInput(
        attrs={'type': 'number', 'id': 'discount', 'oninput': 'limit_input(id, 5)'}),
        label='Скидка, %',
        min_value=0.0,
        max_value=99.99,
        initial=0.0,
    )
    discount_rub = forms.FloatField(widget=NumberInput(
        attrs={'type': 'number', 'id': 'discount_rub', 'oninput': 'limit_input(id, 6)'}),
        label='Скидка, руб.',
        min_value=0.0,
        max_value=999.99,
        initial=0.0,
    )
    increment = forms.FloatField(widget=NumberInput(
        attrs={'type': 'number', 'id': 'increment', 'oninput': 'limit_input(id, 5)'}),
        label='Надбавка, %',
        min_value=0.0,
        max_value=99.99,
        initial=0.0,
    )
    increment_rub = forms.FloatField(widget=NumberInput(
        attrs={'type': 'text', 'id': 'increment_rub', 'oninput': 'limit_input(id, 5)'}),
        label='Надбавка, руб.',
        min_value=0.0,
        max_value=999.99,
        initial=0.0,
    )
    quantity = forms.IntegerField(
        widget=NumberInput(attrs={'type': 'number', 'id': 'quantity', 'oninput': 'limit_input(id, 4)'}),
        label='Количество, шт.',
        min_value=0,
        max_value=9999,
        initial=0,
    )

    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'weight',
            'price',
            'discount',
            'discount_rub',
            'increment',
            'increment_rub',
            'quantity',
            'is_visible',
            'sticker',
            'category',
            'promo_code',
        ]

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        description = cleaned_data.get('description')

        if name == description:
            raise ValidationError(
                "Название не должно совпадать с описанием!"
            )

        return cleaned_data


# Форма для создания категории
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'name',
            'description',
        ]
