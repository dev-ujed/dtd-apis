from rest_framework import serializers
from .models import *


class ProductosSerializer(serializers.ModelSerializer):

    class Meta:
        model = Productos
        fields = ('descripcion', 'marca', 'origen', 'unidad_medida')


class EntradasSerializer(serializers.ModelSerializer):

    class Meta:
        model = Entradas
        fields = ('cantidad',)


class SalidasSerializer(serializers.ModelSerializer):

    class Meta:
        model = Salidas
        fields = ('cantidad',)

