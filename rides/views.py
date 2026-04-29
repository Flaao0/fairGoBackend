from decimal import Decimal

from rest_framework import generics
from rest_framework import status, response
from rest_framework import views
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from users.permissions import IsDriver, IsPassenger

from .models import Ride
from .serializers import RideCreateSerializer, RideListSerializer
from .utils import calculate_distance, calculate_price

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

class RideCreateView(generics.CreateAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideCreateSerializer
    permission_classes = [IsPassenger]

    def perform_create(self, serializer):
        start_lat = serializer.validated_data['start_lat']
        start_lon = serializer.validated_data['start_lon']
        finish_lat = serializer.validated_data['finish_lat']
        finish_lon = serializer.validated_data['finish_lon']

        distance_km = calculate_distance(
            lat1=start_lat,
            lon1=start_lon,
            lat2=finish_lat,
            lon2=finish_lon,
        )
        calculated_price = calculate_price(distance_km)

        serializer.save(
            passenger=self.request.user,
            status=Ride.Status.SEARCHING,
            price=calculated_price,
        )


class AvailableRidesView(generics.ListAPIView):
    queryset = Ride.objects.filter(status=Ride.Status.SEARCHING)
    serializer_class = RideListSerializer
    permission_classes = [IsDriver]


class AcceptRideView(views.APIView):
    permission_classes = [IsDriver]

    def post(self, request, pk):
        ride = get_object_or_404(Ride, pk=pk)

        if ride.status != Ride.Status.SEARCHING:
            return Response(
                {'error': 'Заказ уже взят или отменен'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        ride.driver = request.user
        ride.status = Ride.Status.ACCEPTED
        ride.save()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"ride_{ride.id}",
            {
                "type": "ride_status_update",
                "status": ride.status,
                "ride_id": ride.id
            }
        )

        return Response(
            {'message': 'Заказ принят', 'ride_id': ride.id},
            status=status.HTTP_200_OK,
        )


class FinishRideView(views.APIView):
    permission_classes = [IsDriver]

    def post(self, request, pk):
        ride = get_object_or_404(Ride, pk=pk)

        if ride.status != Ride.Status.ACCEPTED or ride.driver != request.user:
            return Response(
                {'error': 'Поездка недоступна для завершения'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if ride.promocode:
            ride.price = ride.price * (
                Decimal('1') - Decimal(str(ride.promocode.discount_percent)) / Decimal('100.0')
            )
            ride.price = ride.price.quantize(Decimal('0.01'))

        ride.status = Ride.Status.FINISHED
        ride.save()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"ride_{ride.id}",  
            {
                "type": "ride_status_update", 
                "status": ride.status,
                "ride_id": ride.id
            }
        )

        return Response(
            {
                'message': 'Поездка завершена',
                'ride_id': ride.id,
                'final_price': str(ride.price),
            },
            status=status.HTTP_200_OK,
        )


class PassengerHistoryView(generics.ListAPIView):
    permission_classes = [IsPassenger]
    serializer_class = RideListSerializer

    def get_queryset(self):
        return Ride.objects.filter(
            passenger=self.request.user,
            status__in=[Ride.Status.FINISHED, Ride.Status.CANCELED],
        ).order_by('-created_at')
