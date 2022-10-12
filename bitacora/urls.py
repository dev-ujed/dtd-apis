from django.urls import path
from rest_framework.routers import DefaultRouter

from bitacora.views import *

router=DefaultRouter()

router.register('sol/bitacoraServicio', BitacoraServiciosViewSet)

urlpatterns = [

    #path('solicitudes_docs/',include_docs_urls(title='Documentación de Apis')),
]

urlpatterns+=router.urls
