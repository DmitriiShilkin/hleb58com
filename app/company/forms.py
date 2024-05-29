from django import forms
from django.core.validators import EmailValidator

from .validators import phone_number_validator, text_validator


class MessageForm(forms.Form):
    full_name = forms.CharField(
        label='Фамилия Имя Отчество',
        min_length=5,
        max_length=150,
        validators=[text_validator],
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={
            'type': 'text',
            'onkeypress': 'return event.charCode === 0 || /\d/.test(String.fromCharCode(event.charCode))',
        }),
        min_length=10,
        max_length=10,
        label_suffix='',
        label='Номер телефона: +7',
        validators=[phone_number_validator],
    )
    email = forms.EmailField(
        label='Email',
        max_length=150,
        validators=[EmailValidator]
    )
    text = forms.CharField(widget=forms.Textarea(
        attrs={'rows': 10, 'cols': 60, 'placeholder': 'Напишите Ваше сообщение...'}),
        label='Текст сообщения',
        validators=[text_validator],
    )


class DealerForm(forms.Form):
    company_name = forms.CharField(
        label='Наименование организации',
        min_length=3,
        max_length=150,
        validators=[text_validator],
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={
            'type': 'text',
            'onkeypress': 'return event.charCode === 0 || /\d/.test(String.fromCharCode(event.charCode))',
        }),
        label='Номер телефона: +7',
        label_suffix='',
        min_length=10,
        max_length=10,
        validators=[phone_number_validator],
    )
    proposal = forms.FileField(label='Загрузить коммерческое предложение (pdf, Word)')
    text = forms.CharField(widget=forms.Textarea(
        attrs={'rows': 10, 'cols': 60, 'placeholder': 'Напишите Ваше сообщение...'}),
        label='Текст сообщения',
        validators=[text_validator],
    )
