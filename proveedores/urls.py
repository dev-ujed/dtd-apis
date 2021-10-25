from django.urls import path

from .views import send_password

urlpatterns = [
	path('send_password',    send_password,  name="send-password"),
]