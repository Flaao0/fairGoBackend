from decimal import Decimal

from rest_framework import generics
from rest_framework import status
from rest_framework import views
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from users.permissions import IsDriver, IsPassenger

from .models import Ride
from .serializers import RideCreateSerializer, RideListSerializer


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

        final_price = ride.price
        if ride.promocode:
            discount_percent = Decimal(str(ride.promocode.discount_percent))
            final_price = ride.price * (Decimal('1') - discount_percent / Decimal('100'))

        ride.price = final_price
        ride.status = Ride.Status.FINISHED
        ride.save()

        return Response(
            {
                'message': 'Поездка завершена',
                'ride_id': ride.id,
                'final_price': str(final_price),
            },
            status=status.HTTP_200_OK,
        )
