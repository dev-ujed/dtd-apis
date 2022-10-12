from rest_framework import generics, permissions, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.core import serializers, validators
from django.core.exceptions import ValidationError
from django.http import FileResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from .models import *
from .serializers import *


# Create your views here.
class BitacoraServiciosViewSet(viewsets.ModelViewSet):
    authentication_classes  = ()
    permission_classes      = ()
    queryset                = BitacoraServicios.objects.all()
    serializer_class        = BitacoraServiciosSerializer

    def post(self, request):
        unidad          = request.data.get("unidad")
        folio_sistema   = request.data.get("folio_sistema")
        solicitado_por  = request.data.get("solicitado_por")
        folio_interno   = request.data.get("folio_interno")
        fecha           = request.data.get("fecha")
        solicitud       = request.data.get("solicitud")
        diagnostico     = request.data.get("diagnostico")
        material        = request.data.get("material")
        tecnico         = request.data.get("tecnico")
        area            = request.data.get("area")
        supervisor      = request.data.get("supervisor")
        puesto          = request.data.get("puesto")
        recibido_por    = request.data.get("recibido_por")


        data = {
                'unidad':           unidad,
                'folio_sistema':    folio_sistema,
                'solicitado_por':   solicitado_por,
                'folio_interno':    folio_interno,
                'fecha':            fecha,
                'solicitud':        solicitud,
                'diagnostico':      diagnostico,
                'material':         material,
                'tecnico':          tecnico,
                'area':             area,
                'supervisor':       supervisor,
                'puesto':           puesto,
                'recibido_por':     recibido_por
            }

        serializer = BitacoraServiciosSerializer(data = data)
        if serializer.is_valid():
            bit = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)