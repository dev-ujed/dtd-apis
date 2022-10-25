from itertools import product
from rest_framework import serializers
from .models import *


class ProductosSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Productos
        fields = ('id', 'descripcion', 'marca', 'origen', 'unidad_medida')


class EntradasSerializer(serializers.ModelSerializer):
    #descripcion = serializers.SerializerMethodField()
    descripcion = serializers.CharField(source = 'producto.descripcion')

    class Meta:
        model = Entradas
        fields = ('cantidad', 'producto', 'fecha', 'descripcion')
    
    def get_descripcion(self, obj):
        value = Productos.objects.get(id = obj.producto.id).descripcion
        return value


class SalidasSerializer(serializers.ModelSerializer):
    descripcion = serializers.CharField(source = 'producto.descripcion')

    class Meta:
        model = Salidas
        fields = ('cantidad', 'producto', 'fecha', 'descripcion')

        

