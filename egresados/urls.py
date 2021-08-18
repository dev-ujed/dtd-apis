from django.urls import path
#from rest_framework.routers import DefaultRouter
from .apiviews import getDatosAlumnoPorEgresar

urlpatterns = [
	path('getDatosAlumnoPorEgresar/<str:ciclo>/<str:matricula>', getDatosAlumnoPorEgresar.as_view(), name="getDatosAlumnoPorEgresar"),
]