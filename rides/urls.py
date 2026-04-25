from django.urls import path

from .views import (
    AcceptRideView,
    AvailableRidesView,
    FinishRideView,
    PassengerHistoryView,
    RideCreateView,
)

urlpatterns = [
    path('available/', AvailableRidesView.as_view(), name='rides-available'),
    path('history/', PassengerHistoryView.as_view(), name='ride-history'),
    path('<int:pk>/accept/', AcceptRideView.as_view(), name='ride-accept'),
    path('<int:pk>/finish/', FinishRideView.as_view(), name='ride-finish'),
    path('', RideCreateView.as_view(), name='ride-create'),
]
