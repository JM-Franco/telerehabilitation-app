from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

# Register your models here.

class AccountAdmin(UserAdmin):
    ordering = ("email",)
    list_display = (
        "email", 
        "first_name", 
        "last_name", 
        "role", 
        "is_admin", 
        "is_staff", 
        "is_superuser"
    )
    # search_fields = ("email", "first_name", "last_name")
    # readonly_fields = ("id", "date_joined", "last_login")
    readonly_fields = ('date_joined', 'last_login',)

    # filter_horizontal = ()
    # list_filter = ()
    # add_fieldsets = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'birthdate', 'age', 'sex', 'contact_number')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',),
        }),
    )

admin.site.register(Account, AccountAdmin)
admin.site.register(SystemAdmin)
admin.site.register(PhysicalTherapist)
admin.site.register(Patient)
admin.site.register(Account_Request)
