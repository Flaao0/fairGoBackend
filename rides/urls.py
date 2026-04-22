from django.urls import path

from .views import AcceptRideView, AvailableRidesView, RideCreateView

urlpatterns = [
    path('available/', AvailableRidesView.as_view(), name='rides-available'),
    path('<int:pk>/accept/', AcceptRideView.as_view(), name='ride-accept'),
    path('', RideCreateView.as_view(), name='ride-create'),
]
