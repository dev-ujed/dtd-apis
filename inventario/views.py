from rest_framework import status, viewsets
from rest_framework.response import Response
from django.shortcuts import render
from .models import *
from .serializers import *

# Create your views here.
class ProductosViewSet(viewsets.ModelViewSet):
    authentication_classes  = ()
    permission_classes      = ()
    queryset                = Productos.objects.all()
    serializer_class        = ProductosSerializer

class EntradasViewSet(viewsets.ModelViewSet):
    authentication_classes  = ()
    permission_classes      = ()
    queryset                = Entradas.objects.all()
    serializer_class        = EntradasSerializer


    def post(self, request):
        producto    = request.data.get("producto")
        cantidad    = request.data.get("cantidad")
        fecha       = request.data.get("fecha")
        print(fecha)

        data = {
            'producto':  producto,
            'cantidad':  cantidad,
            'fecha':     fecha,
        }

        print(data)
        serializer = EntradasCreateSerializer(data = data)
        if serializer.is_valid():
            ent = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class SalidasViewSet(viewsets.ModelViewSet):
    authentication_classes  = ()
    permission_classes      = ()
    queryset                = Salidas.objects.all()
    serializer_class        = SalidasSerializer


    def post(self, request):
        producto    = request.data.get("producto")
        cantidad    = request.data.get("cantidad")
        fecha       = request.data.get("fecha")

        data = {
            'producto':  producto,
            'cantidad':  cantidad,
            'fecha':     fecha,
        }

        serializer = SalidasCreateDerializer(data = data)
        if serializer.is_valid():
            sal = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)



