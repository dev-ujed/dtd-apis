from django.db import models


# Create your models here.
class DatosAlumnoPorEgresar(models.Model):
    matricula	    	= models.CharField(primary_key=True, max_length=10)
    nombre_completo		= models.CharField(max_length=500)
    nombre		    	= models.CharField(max_length=100)
    paterno		    	= models.CharField(max_length=100)
    materno		    	= models.CharField(max_length=100)
    sexo        		= models.CharField(max_length=10)
    f_nacimiento		= models.CharField(max_length=10)
    cve_estado			= models.CharField(max_length=2)
    estado				= models.CharField(max_length=250)
    cve_municipio		= models.CharField(max_length=5)
    municipio			= models.CharField(max_length=250)
    calle        		= models.CharField(max_length=500)
    colonia        		= models.CharField(max_length=500)
    telefono	    	= models.CharField(max_length=13)
    celular 	    	= models.CharField(max_length=13)
    cve_escuela			= models.CharField(max_length=4)
    escuela				= models.CharField(max_length=250)
    cve_carrera			= models.CharField(max_length=6)
    carrera				= models.CharField(max_length=250)

    def __str__(self):
        return '{}'.format(...)

    class Meta:
        app_label = 'egresados'
        managed = False
