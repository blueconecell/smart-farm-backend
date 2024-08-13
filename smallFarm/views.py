from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from .models import SmallFarm,SoilSample,MoistureSensor
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
                    serializer.save()
                    return Response(serializer.data)
            except Exception as e:
                return Response({"test error(valid_error)":str(e)})
        except Exception as e:
            return Response({"test error(data error)":str(e)})
        
class AllSoilSampleView(APIView):
    def get(self, request):
        try:
            soilSamples = SoilSample.objects.all()
            serializer = serializers.SoilSampleSerializer(soilSamples,many=True,)
            return Response(serializer.data)
        except Exception as e:
            return Response({"에러":str(e)})
    def post(self, request):
        try:
            serializer = serializers.SoilSampleSerializer(data = request.data)
            try:
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
            except Exception as e:
                return Response({"test error(valid_error)":str(e)})
        except Exception as e:
            return Response({"test error(data error)":str(e)})
class SoilSampleDetailsView(APIView):
    def get_object(self, soilSamplePK):
        try:
            return SoilSample.objects.get(id=soilSamplePK)
        except SoilSample.DoesNotExist:
            raise NotFound(detail="SoilSample not found.")

    def get(self, request, soilSamplePK):
        try:
            soilSample = self.get_object(soilSamplePK)
            moisture_sensors = MoistureSensor.objects.filter(soil_sample=soilSample)
            if not moisture_sensors.exists():
                return Response({"detail": "No MoistureSensors found for this SoilSample."}, status=status.HTTP_204_NO_CONTENT)
            
            serializer = serializers.MoistureSensorSerializer(moisture_sensors, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except MoistureSensor.DoesNotExist:
            return Response({"detail": "Error retrieving MoistureSensor data."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class AllMoistureSensorView(APIView):
    def get(self, request):
        try:
            moistureSensors = MoistureSensor.objects.all()
            serializer = serializers.MoistureSensorSerializer(moistureSensors,many=True,)
            return Response(serializer.data)
        except Exception as e:
            return Response({"에러":str(e)})
    def post(self, request):
        try:
            serializer = serializers.MoistureSensorSerializer(data = request.data)
            try:
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
            except Exception as e:
                return Response({"test error(valid_error)":str(e)})
        except Exception as e:
            return Response({"test error(data error)":str(e)})
