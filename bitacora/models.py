from django.db import models

# Create your models here.

class BitacoraServicios(models.Model):
    unidad          = models.CharField(max_length=40)
    folio_sistema   = models.CharField(max_length=40)
    solicitado_por  = models.CharField(max_length=40)
    folio_interno   = models.CharField(max_length=40)
    fecha           = models.DateField(auto_now_add=True, null=True)
    solicitud       = models.CharField(max_length=200)
    diagnostico     = models.CharField(max_length=200)
    material        = models.CharField(max_length=200)
    tecnico         = models.CharField(max_length=60)
    area            = models.CharField(max_length=60)
    supervisor      = models.CharField(max_length=60)
    puesto          = models.CharField(max_length=60)
    recibido_por    = models.CharField(max_length=60)