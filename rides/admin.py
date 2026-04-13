from django.contrib import admin

from .models import RecentAddress, Ride


@admin.register(RecentAddress)
class RecentAddressAdmin(admin.ModelAdmin):
    list_display = ('address_text', 'user', 'lat', 'lon')


@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'passenger',
        'driver',
        'status',
        'price',
        'created_at',
    )
    list_filter = ('status',)
