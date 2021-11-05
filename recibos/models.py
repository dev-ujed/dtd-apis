from django.db import models

# Create your models here.
class TNFactura(models.Model):
    tfac_id             = models.IntegerField(primary_key=True)
    tfac_nomina         = models.CharField(max_length=2)
    tfac_periodo        = models.CharField(max_length=7)
    tfac_ures           = models.CharField(max_length=8)
    tfac_sfdo           = models.CharField(max_length=8)
    tfac_prog           = models.CharField(max_length=8)
    tfac_matricula      = models.CharField(max_length=8)
    tfac_estatus        = models.CharField(max_length=1)

    class Meta:
        db_table    = 'tnfactura'
        app_label   = 'recibos_nom'
        managed     = False



class TNArchivo(models.Model):
    tarc_id             = models.IntegerField(primary_key=True)
    tarc_nombre_pdf     = models.CharField(max_length=100)
    tarc_archivo_pdf    = models.BinaryField()
    
    class Meta:
        db_table    = 'tnarchivo'
        app_label   = 'recibos_nom'
        managed     = False
