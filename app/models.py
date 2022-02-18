from django.db import models


# Create your models here.


class BtcValue(models.Model):
    date = models.DateTimeField()
    value = models.FloatField()

    class Meta:
        indexes = [
            models.Index(fields=['date'])
        ]
