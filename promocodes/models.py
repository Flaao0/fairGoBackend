from django.db import models


class Promocode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_percent = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
