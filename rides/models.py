from django.conf import settings
from django.db import models


class RecentAddress(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recent_addresses',
    )
    address_text = models.CharField(max_length=255)
    lat = models.FloatField()
    lon = models.FloatField()

    def __str__(self):
        return f'{self.address_text}'


class Ride(models.Model):
    class Status(models.TextChoices):
        CREATED = 'CREATED', 'Created'
        SEARCHING = 'SEARCHING', 'Searching'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        IN_PROGRESS = 'IN_PROGRESS', 'In progress'
        FINISHED = 'FINISHED', 'Finished'
        CANCELED = 'CANCELED', 'Canceled'

    passenger = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='rides_as_passenger',
    )
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='rides_as_driver',
    )
    start_lat = models.FloatField()
    start_lon = models.FloatField()
    finish_lat = models.FloatField()
    finish_lon = models.FloatField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.CREATED,
    )
    price = models.DecimalField(max_digits=8, decimal_places=2)
    promocode = models.ForeignKey(
        'promocodes.Promocode',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Ride {self.pk} ({self.status})'
