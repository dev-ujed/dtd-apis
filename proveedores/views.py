from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from rest_framework.decorators import api_view, authentication_classes, permission_classes


# Create your views here.
def send_email(request, data, email, subject, email_template_name):
    body = render_to_string(email_template_name, data, request=request)
    from_email = 'Padrón de Proveedores UJED <registroproveedores@ujed.mx>'
    to = email

    email = EmailMessage(
        subject    = subject,
        body       = body,
        from_email = from_email,
        to         = [to]
        )
    email.content_subtype = 'html'
    email.send()



@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def send_password(request):
    send_email(request,
                {
                    'rfc_provider'      : request.data['rfc'],
                    'pass_provider'     : request.data['pass']
                }, 
                request.data['email'], 
                'Activación de Usuario del Padrón de Proveedores UJED', 
                'emails/provider_password.mjml')
    return HttpResponse('terminó')
