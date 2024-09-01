from django.db import models

from teams.models import Team

# Create your models here.
class SmallFarm(models.Model):
    name = models.CharField(max_length=300)
    soil_humid=models.FloatField()
    def __str__(self):
        return self.name

class SoilSample(models.Model):
    team = models.ForeignKey(Team, related_name='soil_samples', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.name} => {self.team.name}"
    
class MoistureSensor(models.Model):
    soil_sample = models.ForeignKey(SoilSample, related_name='moisture_sensors', on_delete=models.CASCADE)
    humidValue = models.FloatField(null=True, blank=True)
    measured_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.soil_sample.name} => 측정값 : {self.humidValue} "
    

class GasAreaSample(models.Model):
    team = models.ForeignKey(Team, related_name='gasArea_samples', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.name} => {self.team.name}"
    
class GasSensor(models.Model):
    gasArea_sample = models.ForeignKey(GasAreaSample, related_name='gas_sensors', on_delete=models.CASCADE)
    gasValue = models.FloatField(null=True, blank=True)
    measured_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.gasArea_sample.name} => 측정값 : {self.gasValue} "