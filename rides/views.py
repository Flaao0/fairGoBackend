from decimal import Decimal

from rest_framework import generics

from users.permissions import IsPassenger

from .models import Ride
from .serializers import RideCreateSerializer


class RideCreateView(generics.CreateAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideCreateSerializer
    permission_classes = [IsPassenger]

    def perform_create(self, serializer):
        serializer.save(
            passenger=self.request.user,
            status=Ride.Status.SEARCHING,
            price=Decimal('500.00'),
        )
