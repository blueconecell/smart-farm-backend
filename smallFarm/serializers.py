from rest_framework.serializers import ModelSerializer
from .models import SmallFarm,SoilSample,MoistureSensor

class SmallFarmSerializer(ModelSerializer):

    class Meta:
        model = SmallFarm
        fields = "__all__"

class SoilSampleSerializer(ModelSerializer):

    class Meta:
        model = SoilSample
        fields = "__all__"


class MoistureSensorSerializer(ModelSerializer):

    class Meta:
        model = MoistureSensor
        fields = "__all__"
