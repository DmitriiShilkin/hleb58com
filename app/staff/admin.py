from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Staff


class StaffUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        ('Дополнительная информация', {
            'fields': (
                'middle_name',
                'position',
                'contract',
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
                'position',
                'contract',
                'birthdate',
                'city',
                'phone',
                'telegram',
                'whatsapp',
                'viber',
                )}),
    )


admin.site.register(Staff, StaffUserAdmin)
