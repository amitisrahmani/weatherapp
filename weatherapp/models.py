from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100, unique=True)  # City name
    temperature = models.FloatField(null=True, blank=True)  # Store temperature
    description = models.CharField(max_length=255, null=True, blank=True)  # Weather description
    icon = models.CharField(max_length=50, null=True, blank=True)  # Icon code for weather image
    last_updated = models.DateTimeField(auto_now=True)  # Timestamp of last update

    def __str__(self):
        return self.name
