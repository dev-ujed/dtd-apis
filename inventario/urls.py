from django.urls import path
from rest_framework.routers import DefaultRouter
from inventario.views import *

router=DefaultRouter()

router.register('sol/productos',        ProductosViewSet)
router.register('sol/inventario_ent',   EntradasViewSet)
router.register('sol/inventario_sal',   SalidasViewSet)

urlpatterns = [

]

urlpatterns+=router.urls
