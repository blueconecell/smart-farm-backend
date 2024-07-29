from rest_framework.serializers import ModelSerializer
from .models import SmallFarm

class SmallFarmSerializer(ModelSerializer):

    class Meta:
        model = SmallFarm
        fields = "__all__"
