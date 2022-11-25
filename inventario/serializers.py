from rest_framework import serializers
from .models import *


class ProductosSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Productos
        fields = ('id', 'descripcion', 'marca', 'origen', 'unidad_medida')


class EntradasSerializer(serializers.ModelSerializer):
    descripcion = serializers.CharField(source = 'producto.descripcion', trim_whitespace=True, required=False,allow_blank=True, allow_null=True)

    class Meta:
        model = Entradas
        fields = ('cantidad', 'producto', 'fecha', 'descripcion')
        
        
class SalidasSerializer(serializers.ModelSerializer):
    descripcion = serializers.CharField(source = 'producto.descripcion', trim_whitespace=True, required=False,allow_blank=True, allow_null=True)

    class Meta:
        model = Salidas
        fields = ('cantidad', 'producto', 'fecha', 'descripcion')

class EntradasCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entradas
        fields = ('cantidad', 'producto', 'fecha')
        

class SalidasCreateDerializer(serializers.ModelSerializer):

    class Meta:
        model = Salidas
        fields = ('cantidad', 'producto', 'fecha')
 
