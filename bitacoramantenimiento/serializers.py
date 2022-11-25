from rest_framework import serializers
from .models import *

class BitacoraMantenimientoSerializers(serializers.ModelSerializer):

    class Meta:
        model = BitacoraMantenimiento
        fields = ('id', 'matricula', 'area')


class FechasMantenimientoSerializers(serializers.ModelSerializer):

    class Meta:
        model = FechasMantenimiento
        fields = ('bitacora', 'ult_mant', 'nuevo_mant')