from rest_framework.routers import DefaultRouter
from bitacoramantenimiento.views import *

router=DefaultRouter()

router.register('sol/bitacora_mant', BitacoraMantenimientoViewSet)
router.register('sol/fechas_mant',   FechasMantenimientoViewSet)


urlpatterns = []

urlpatterns+=router.urls
