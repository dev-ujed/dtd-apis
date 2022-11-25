from rest_framework import status, viewsets
from rest_framework.response import Response
from django.shortcuts import render
from .models import *
from .serializers import *

# Create your views here.
class BitacoraMantenimientoViewSet(viewsets.ModelViewSet):
    authentication_classes  = ()
    permission_classes      = ()
    queryset                = BitacoraMantenimiento.objects.all()
    serializer_class        = BitacoraMantenimientoSerializers


class FechasMantenimientoViewSet(viewsets.ModelViewSet):
    authentication_classes  = ()
    permission_classes      = ()
    queryset                = FechasMantenimiento.objects.all()
    serializer_class        = FechasMantenimientoSerializers
