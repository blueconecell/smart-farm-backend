from django.db import models

# Create your models here.
class SmallFarm(models.Model):
    name = models.CharField(max_length=300)
    soil_humid=models.FloatField()