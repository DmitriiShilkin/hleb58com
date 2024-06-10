from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class BaseRegisterForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "username",
            "last_name",
            "first_name",
            "password1",
            "password2",
        )


class CustomUserUpdateForm(UserChangeForm):
    email = forms.EmailField(
        # widget=forms.TextInput(attrs={'readonly': True}),
        disabled=True
    )
    username = forms.CharField(
        # widget=forms.TextInput(attrs={'readonly': True}),
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
        model = CustomUser
        fields = (
            "email",
            "username",
            "last_name",
            "first_name",
            "middle_name",
            "individual_taxpayer_number",
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
        # self.fields["password"].help_text = None
