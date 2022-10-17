from random import choices
from django.db import models

# Create your models here.
class Productos(models.Model):
    UNIDAD_MEDIDAS  = (
        ('pzs', 'piezas'),
        ('mts', 'metros'),
    )
    descripcion     = models.CharField(max_length=90)
    marca           = models.CharField(max_length=60)
    origen          = models.CharField(max_length=60)
    unidad_medida   = models.CharField(max_length=3, choices=UNIDAD_MEDIDAS)


class Entradas(models.Model):
    producto    = models.ForeignKey(Productos, on_delete=models.CASCADE)
    cantidad    = models.FloatField()
    fecha       = models.DateField(auto_now_add=True, null=True)


class Salidas(models.Model):
    producto    = models.ForeignKey(Productos, on_delete=models.CASCADE)
    cantidad    = models.FloatField()
    fecha       = models.DateField(auto_now_add=True, null=True)



