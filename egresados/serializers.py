from rest_framework import serializers
from .models import DatosAlumnoPorEgresar

class DatosAlumnoPorEgresarSerializer(serializers.ModelSerializer):
	class Meta:
		model = DatosAlumnoPorEgresar
		fields = '__all__'