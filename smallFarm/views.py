from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SmallFarm
from . import serializers
# Create your views here.
class AllSmallFarm(APIView):
    def get(self, request):
        try:
            smallFarms = SmallFarm.objects.all()
            serializer = serializers.SmallFarmSerializer(smallFarms,many=True,)
            return Response(serializer.data)
        except Exception as e:
            return Response({"에러":str(e)})
    def post(self, request):
        try:
            serializer = serializers.SmallFarmSerializer(data = request.data)
            try:
                if serializer.is_valid():
                    farmData = serializer.save()
                    return Response(serializer.data)
            except Exception as e:
                return Response({"test error(valid_error)":str(e)})
        except Exception as e:
            return Response({"test error(data error)":str(e)})