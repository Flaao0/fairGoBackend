from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    is_driver = models.BooleanField(default=False)
    rating = models.FloatField(default=5.0)
