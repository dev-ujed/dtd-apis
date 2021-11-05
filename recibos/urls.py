from django.urls import path

from .views import *

urlpatterns = [
	path('get_recibos_pdf',		get_recibos_nomina,  name="get-pay-slips"),
]