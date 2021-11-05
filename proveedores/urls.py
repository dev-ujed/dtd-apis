from django.urls import path

from .views import send_password, send_review

urlpatterns = [
	path('send_password',	send_password,  name="send-password"),
	path('send_review',    	send_review,	name="send-review"),
]