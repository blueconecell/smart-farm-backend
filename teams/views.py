from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Team
from . import serializers
# Create your views here.
class TeamView(APIView):
    def get(self, request):
        try:
            teams = Team.objects.all()
            serializer = serializers.TeamSerializer(teams,many=True,)
            return Response(serializer.data)
        except Exception as e:
            return Response({"에러":str(e)})
    def post(self, request):
        try:
            serializer = serializers.TeamSerializer(data = request.data)
            try:
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
            except Exception as e:
                return Response({"test error(valid_error)": str(e)})
        except Exception as e:
            return Response({"test error(data error)": str(e)})