from django.urls import path

from .views import RideCreateView

urlpatterns = [
    path('', RideCreateView.as_view(), name='ride-create'),
]
