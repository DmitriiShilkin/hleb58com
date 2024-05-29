from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Staff


class StaffRegisterForm(UserCreationForm):
    phone = forms.CharField(
        widget=forms.TextInput(attrs={
            'type': 'text',
            'onkeypress': 'return event.charCode === 0 || /\d/.test(String.fromCharCode(event.charCode))',
        }),
        label="Номер телефона: +7",
        label_suffix="",
        min_length=11,
        max_length=12,
        required=False,
    )
    birthdate = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
        }, format='%Y-%m-%d'),
        label="Дата рождения",
        required=False
    )

    class Meta:
        model = Staff
        fields = (
            "email",
            "username",
            "last_name",
            "first_name",
            "middle_name",
            "position",
            "contract",
            "birthdate",
            "city",
            "phone",
            "password1",
            "password2",
        )


class StaffUpdateForm(UserChangeForm):
    email = forms.EmailField(
        disabled=True
    )
    username = forms.CharField(
        label="Имя пользователя",
        disabled=True
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={
            'type': 'text',
            'onkeypress': 'return event.charCode === 0 || /\d/.test(String.fromCharCode(event.charCode))',
        }),
        label="Номер телефона: +7",
        label_suffix="",
        min_length=11,
        max_length=12,
        required=False,
    )
    birthdate = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
        }, format='%Y-%m-%d'),
        label="Дата рождения",
        required=False
    )

    class Meta:
        model = Staff
        fields = (
            "email",
            "username",
            "last_name",
            "first_name",
            "middle_name",
            "position",
            "contract",
            "groups",
            "birthdate",
            "city",
            "phone",
            "telegram",
            "whatsapp",
            "viber",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields["password"]
