from django.contrib import admin

from .models import Promocode


@admin.register(Promocode)
class PromocodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'is_active')
