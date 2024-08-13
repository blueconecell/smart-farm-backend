from django.contrib import admin
from .models import SmallFarm,SoilSample,MoistureSensor
# Register your models here.
@admin.register(SmallFarm)
class SmallFarmAdmin(admin.ModelAdmin):
    list_display=(
        "name","soil_humid"
    )

@admin.register(SoilSample)
class SoilSampleAdmin(admin.ModelAdmin):
    list_display=(
        "team","name","location","created_at"
    )

@admin.register(MoistureSensor)
class MoistureSensorAdmin(admin.ModelAdmin):
    list_display=(
        "soil_sample","humidValue","measured_at"
    )