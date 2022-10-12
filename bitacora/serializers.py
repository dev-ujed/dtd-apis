from dataclasses import field
from pyexpat import model
from rest_framework import serializers
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.text import slugify

from .models import *
import datetime, os

class BitacoraServiciosSerializer(serializers.ModelSerializer):

    class Meta:
        model = BitacoraServicios
        fields = ('unidad', 'folio_sistema', 'solicitado_por',
        'folio_interno', 'solicitud', 'diagnostico', 'material',
        'tecnico', 'area', 'supervisor', 'puesto', 'recibido_por')