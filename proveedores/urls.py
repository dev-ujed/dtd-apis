from django.urls import path

from .views import send_password

urlpatterns = [
	path('send_password/<str:email_provider>/<str:rfc_provider>/<str:pass_provider>',    send_password,  name="send-password"),
]