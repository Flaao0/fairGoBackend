from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('FairGo', {'fields': ('phone_number', 'is_driver', 'rating')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('phone_number', 'is_driver', 'rating')}),
    )
    list_display = BaseUserAdmin.list_display + ('phone_number', 'is_driver', 'rating')
