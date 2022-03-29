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
    search_fields = ("email", "first_name", "last_name")
    readonly_fields = ("id", "date_joined", "last_login")

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)
admin.site.register(SystemAdmin)
admin.site.register(PhysicalTherapist)
admin.site.register(Patient)