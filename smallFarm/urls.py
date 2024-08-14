from django.urls import path
from . import views

urlpatterns = [
    path("SmallFarm", views.AllSmallFarm.as_view()),
    path("SoilSample", views.AllSoilSampleView.as_view()),
    path("SoilSample/<str:soilSamplePK>", views.SoilSampleDetailsView.as_view()),
    path("MoistureSensor", views.AllMoistureSensorView.as_view()),
]
