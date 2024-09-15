from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from .models import SmallFarm,SoilSample,MoistureSensor,GasAreaSample,GasSensor
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
    
# 토양수분도 학습 모듈
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

# DIY 온실가스 측정기
class AllGasAreaSampleView(APIView):
    def get(self, request):
        try:
            gasAreaSamples = GasAreaSample.objects.all()
            serializer = serializers.GasAreaSampleSerializer(gasAreaSamples,many=True,)
            return Response(serializer.data)
        except Exception as e:
            return Response({"에러":str(e)})
    def post(self, request):
        try:
            serializer = serializers.GasAreaSampleSerializer(data = request.data)
            if serializer.is_valid():
                try:
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response({"test error(valid_error)": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"test error(data error)": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class GasAreaSampleDetailsView(APIView):
    def get_object(self, gasAreaSamplePK):
        try:
            return GasAreaSample.objects.get(id=gasAreaSamplePK)
        except GasAreaSample.DoesNotExist:
            raise NotFound(detail="GasAreaSample not found.")

    def get(self, request, gasAreaSamplePK):
        try:
            GasAreaSample = self.get_object(gasAreaSamplePK)
            gasSensors = GasSensor.objects.filter(gasArea_sample=GasAreaSample)
            if not gasSensors.exists():
                return Response({"detail": "No gasSensors found for this GasAreaSample."}, status=status.HTTP_204_NO_CONTENT)
            
            serializer = serializers.GasSensorSerializer(gasSensors, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except GasSensor.DoesNotExist:
            return Response({"detail": "Error retrieving gasSensors data."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class AllGasSensorView(APIView):
    def get(self, request):
        try:
            gasSensors = GasSensor.objects.all()
            serializer = serializers.GasSensorSerializer(gasSensors,many=True,)
            return Response(serializer.data)
        except Exception as e:
            return Response({"에러":str(e)})
    def post(self, request):
        try:
            serializer = serializers.GasSensorSerializer(data = request.data)
            try:
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
            except Exception as e:
                return Response({"test error(valid_error)":str(e)})
        except Exception as e:
            return Response({"test error(data error)":str(e)})
        
class LatestGasValue(APIView):
    def get(self,request):
        try:
            all_gas_sensors = GasSensor.objects.all().order_by('-measured_at')
            latest_gas_values = {}
            # 최신 값만 유지하는 루프
            for sensor in all_gas_sensors:
                # 해당 gasArea_sample에 대한 값이 없으면 추가
                if sensor.gasArea_sample_id not in latest_gas_values:
                    latest_gas_values[sensor.gasArea_sample_id] = {
                        'gasArea_sample_pk': sensor.gasArea_sample.pk,
                        'gasArea_sample_name': sensor.gasArea_sample.name,
                        'gasValue': sensor.gasValue,
                        'measured_at': sensor.measured_at,
                    }
            data = list(latest_gas_values.values())
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"LatestGasValue error":str(e)})