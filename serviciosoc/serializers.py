from rest_framework import serializers

from .models import DatosAlumno, DatosAlumnos, ContarAlumnos, DBAlumnos, \
					DBMovAlumnos, DBCiclo, Estadistica, Matriculas, UltimoMovAlumno


class AlumnoSerializer(serializers.ModelSerializer):
	class Meta:
		model = DatosAlumno
		fields = '__all__'



class AlumnosSerializer(serializers.ModelSerializer):
	class Meta:
		model = DatosAlumnos
		fields = '__all__'



class ContarSerializer(serializers.ModelSerializer):
	class Meta:
		model = ContarAlumnos
		fields = '__all__'



class MatriculasSerializer(serializers.ModelSerializer):
	# matricula	= serializers.CharField(max_length=9)
	class Meta:
		model = Matriculas
		fields = '__all__'



class EstadisticaSerializer(serializers.ModelSerializer):
	ciclo		= serializers.CharField(max_length=3)
	ciclo_desc	= serializers.CharField(max_length=6)
	activos		= MatriculasSerializer(many=True)
	inactivos	= MatriculasSerializer(many=True)
	
	class Meta:
		model = Estadistica
		fields = '__all__'



class DBAlumnosSerializer(serializers.ModelSerializer):
	class Meta:
		model = DBAlumnos
		fields = '__all__'



class DBMovAlumnosSerializer(serializers.ModelSerializer):
	class Meta:
		model = DBMovAlumnos
		fields = '__all__'



class DBCicloSerializer(serializers.ModelSerializer):
	class Meta:
		model = DBCiclo
		fields = ('ciclo','ciclo_desc')#'__all__'



class UltimoMovAlumnoSerializer(serializers.ModelSerializer):
	class Meta:
		model = UltimoMovAlumno
		fields = '__all__'#('matricula', 'fecha_mov')
