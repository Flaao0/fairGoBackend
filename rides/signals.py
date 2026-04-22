from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Ride


@receiver(post_save, sender=Ride)
def send_ride_status_update(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'ride_{instance.id}',
        {
            'type': 'ride_status_update',
            'data': {
                'ride_id': instance.id,
                'status': instance.status,
            },
        },
    )
