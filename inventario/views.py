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

    def post(self, request):
        descripcion     = request.data.get("descripcion")
        marca           = request.data.get("marca")
        origen          = request.data.get("origen")
        unidad_medida   = request.data.get("unidad_medida")

        data = {
                'descripcion':      descripcion,
                'marca':            marca,
                'origen':           origen,
                'unidad_medida':    unidad_medida,

            }
        print(data)
        serializer = ProductosSerializer(data = data)
        if serializer.is_valid():
            prod = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class AllProductsViewSet(viewsets.ModelViewSet):
    authentication_classes  = ()
    permission_classes      = ()
    queryset = Productos.objects.all()
    serializer_class = ProductosSerializer

class EntradasViewSet(viewsets.ModelViewSet):
    authentication_classes  = ()
    permission_classes      = ()
    queryset                = Entradas.objects.all()
    serializer_class        = EntradasSerializer


    def post(self, request):
        descripcion    = request.data.get("descripcion")
        cantidad    = request.data.get("cantidad")
        fecha       = request.data.get("fecha")
        print(fecha)

        data = {
            'descripcion':  descripcion,
            'cantidad':  cantidad,
            'fecha':     fecha,
        }

        print(data)
        serializer = EntradasSerializer(data = data)
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

        serializer = SalidasSerializer(data = data)
        if serializer.is_valid():
            sal = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)



