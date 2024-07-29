from django.contrib import admin
from .models import SmallFarm
# Register your models here.
@admin.register(SmallFarm)
class SmallFarmAdmin(admin.ModelAdmin):
    list_display=(
        "name","soil_humid"
    )