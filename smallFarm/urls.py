from django.urls import path
from . import views

urlpatterns = [
    path("allSmallFarm", views.AllSmallFarm.as_view()),
    path("allSoilSample", views.AllSoilSampleView.as_view()),
    path("allSoilSample/<str:soilSamplePK>", views.SoilSampleDetailsView.as_view()),
    path("allMoistureSensor", views.AllMoistureSensorView.as_view()),
]
