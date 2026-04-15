from rest_framework import serializers

from .models import Ride


class RideCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = (
            'id',
            'start_lat',
            'start_lon',
            'finish_lat',
            'finish_lon',
            'promocode',
        )
        read_only_fields = ('id',)
