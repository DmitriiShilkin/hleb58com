from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, OneTimeCode


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        ('Дополнительная информация', {
            'fields': (
                'middle_name',
                'individual_taxpayer_number',
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
                'last_name',
                'first_name',
                'middle_name',
                'individual_taxpayer_number',
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
