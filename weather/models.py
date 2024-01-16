from django.db import models

class Weather(models.Model):
    city = models.CharField(max_length=255, unique=True)
    temperature = models.FloatField()
    pressure = models.FloatField()
    wind_speed = models.FloatField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)  

    def __str__(self):
        return self.city