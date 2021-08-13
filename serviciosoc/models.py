from django.db import models


# Create your models here.
class DatosAlumnos(models.Model):
	matricula		= models.CharField(primary_key=True, max_length=9)
	nombre			= models.CharField(max_length=35)
	paterno			= models.CharField(max_length=20)
	materno			= models.CharField(max_length=20)

	def __str__(self):
		return '{}'.format(...)

	class Meta:
		managed = False



class DatosAlumno(models.Model):
	matricula		= models.CharField(primary_key=True, max_length=9)
	nombre			= models.CharField(max_length=35)
	paterno			= models.CharField(max_length=20)
	materno			= models.CharField(max_length=20)
	email			= models.CharField(max_length=50)
	telefono		= models.CharField(max_length=15)
	ingreso_cve		= models.CharField(max_length=3)
	ingreso_desc	= models.CharField(max_length=6)
	actual_cve		= models.CharField(max_length=3)
	actual_desc		= models.CharField(max_length=6)
	actual_semestre	= models.IntegerField()
	actual_estatus	= models.IntegerField()
	actual_destatus	= models.CharField(max_length=20)
	egreso_cve		= models.CharField(max_length=3)
	egreso_desc		= models.CharField(max_length=6)
	ultimo_cve		= models.CharField(max_length=3)
	ultimo_desc		= models.CharField(max_length=6)
	ultimo_semestre	= models.IntegerField()
	ultimo_estatus	= models.IntegerField()
	ultimo_destatus	= models.CharField(max_length=20)

	def __str__(self):
		return '{}'.format(...)

	class Meta:
		managed = False



class ContarAlumnos(models.Model):
	escuela		= models.IntegerField(primary_key=True)
	total		= models.IntegerField()
	activos		= models.IntegerField()
	bajas		= models.IntegerField()

	def __str__(self):
		return '{}'.format(self.escuela, self.total, self.activos, self.bajas)

	class Meta:
		managed = False



class Matriculas(models.Model):
	matricula	= models.CharField(primary_key=True, max_length=9)

	def __str__(self):
		return '{}'.format(...)
	
	class Meta:
		managed = False



class Estadistica(models.Model):
	ciclo		= models.CharField(primary_key=True, max_length=3)
	ciclo_desc	= models.CharField(max_length=6)
	
	def __str__(self):
		return '{}{}'.format(...)

	class Meta:
		managed = False



class DBAlumnos(models.Model):
	matricula			= models.CharField(primary_key=True, max_length=9, db_column='cve_alumno')
	nombre				= models.CharField(max_length=35)
	paterno				= models.CharField(max_length=20)
	materno				= models.CharField(max_length=20)
	f_nacimiento		= models.DateField()
	calle				= models.CharField(max_length=30)
	colonia				= models.CharField(max_length=30)
	telefono			= models.CharField(max_length=15)
	esc_procedencia		= models.CharField(max_length=45)
	cve_procedencia		= models.IntegerField()
	cve_usuario			= models.CharField(max_length=32)
	cve_edo_nac			= models.CharField(max_length=2)
	cve_mun_nac			= models.CharField(max_length=5)
	est_civil			= models.CharField(max_length=7)
	trabaja				= models.CharField(max_length=1)
	extranjero			= models.CharField(max_length=1)
	sexo				= models.CharField(max_length=9)
	cve_edo_pro			= models.CharField(max_length=2)
	cve_mun_pro			= models.CharField(max_length=5)
	f_ing_inst			= models.DateField()
	cer_sec				= models.CharField(max_length=1)
	cer_pre				= models.CharField(max_length=1)
	cta_bc				= models.CharField(max_length=1)
	fotos				= models.CharField(max_length=1)
	acta_nac			= models.CharField(max_length=1)
	observacion			= models.CharField(max_length=300)
	curp				= models.CharField(max_length=18)
	codigo				= models.CharField(max_length=10)
	correo				= models.CharField(max_length=50)
	ciudad				= models.CharField(max_length=50)
	tel_cel				= models.CharField(max_length=15)
	tel_ofi				= models.CharField(max_length=15)
	area				= models.CharField(max_length=4)
	len_ind				= models.CharField(max_length=1)
	discapacidad		= models.IntegerField()
	cve_region			= models.IntegerField()
	alumno_id			= models.IntegerField()
	aplica_promedio		= models.IntegerField()
	pertenece_comunidad	= models.CharField(max_length=1)
	comunidad_indigena	= models.CharField(max_length=60)
	tipo_disc			= models.CharField(max_length=1)
	apoyo				= models.CharField(max_length=1)
	credencial			= models.CharField(max_length=1)
	num_cred			= models.CharField(max_length=20)
	rfc					= models.CharField(max_length=13)
	becado				= models.CharField(max_length=1)
	
	def __str__(self):
		return '{}'.format(...)

	class Meta:
		managed		= False
		db_table	= 'alumno'



class DBCiclo(models.Model):
	ciclo			= models.IntegerField(primary_key=True, db_column='cve_ciclo')
	desc_ciclo		= models.CharField(max_length=16)
	f_inicial		= models.DateField()
	f_final			= models.DateField()
	cve_tipo_ciclo	= models.IntegerField()
	#ciclo_desc		= models.CharField(max_length=6)

	@property
	def ciclo_desc(self):
		aux = ''
		if self.desc_ciclo[5:6] == 'E':
			aux = 'A'
		else:
			aux = 'B'
		return self.desc_ciclo[0:4] + ' ' + aux

	def __str__(self):
		return '{}'.format(self.ciclo, self.ciclo_desc)

	class Meta:
		managed		= False
		db_table	= 'ciclo'



class DBMovAlumnos(models.Model):
	matricula		= models.CharField(primary_key=True, max_length=9, db_column='cve_alumno')
	ciclo			= models.IntegerField(db_column='cve_ciclo')
	estatus			= models.IntegerField(db_column='cve_estatus')
	fecha_mov		= models.DateField()
	#cve_carrera		= models.CharField(max_length=8)
	escuela			= models.CharField(max_length=8, db_column='cve_escuela')
	semestre		= models.IntegerField()
	#cve_plan		= models.CharField(max_length=5)
	#cve_grupo		= models.CharField(max_length=5)
	#no_incluir		= models.CharField(max_length=1)

	def __str__(self):
		return '{}'.format(...)#

	class Meta:
		managed		= False
		db_table	= 'mov_alumno'



class UltimoMovAlumno(models.Model):
	matricula		= models.CharField(primary_key=True, max_length=9,  db_column='cve_alumno')
	fecha_mov		= models.DateField()
	
	def __str__(self):
		return '{}'.format(...)

	class Meta:
		managed		= False
		get_latest_by = 'fecha_mov'
