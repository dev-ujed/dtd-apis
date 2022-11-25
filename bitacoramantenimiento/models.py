from django.db import models

# Create your models here.
class BitacoraMantenimiento(models.Model):
    matricula   = models.IntegerField()
    area        = models.CharField(max_length=60)


class FechasMantenimiento(models.Model):
    bitacora        = models.ForeignKey(BitacoraMantenimiento, on_delete=models.CASCADE)    
    descripcion     = models.TextField()
    ult_mant        = models.DateField(auto_now_add=True, null=True)

