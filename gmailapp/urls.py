from django.urls import path

from .views import agregar

urlpatterns = [
    path('agregar-cuenta',   agregar,  name="add-account")
]
