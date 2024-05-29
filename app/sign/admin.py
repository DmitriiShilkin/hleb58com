from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, OneTimeCode


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        ('Дополнительная информация', {
            'fields': (
                'middle_name',
                'birthdate',
                'city',
                'phone',
                'telegram',
                'whatsapp',
                'viber',
                )}),
    )
    add_fieldsets = (
        *UserAdmin.add_fieldsets,
        (None, {
            'fields': (
                'email',
                'first_name',
                'last_name',
                'middle_name',
                'birthdate',
                'city',
                'phone',
                'telegram',
                'whatsapp',
                'viber',
                )}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(OneTimeCode)
