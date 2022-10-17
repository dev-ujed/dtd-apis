from rest_framework import status, views, viewsets
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

        serializer = ProductosSerializer(data = data)
        if serializer.is_valid():
            bit = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)