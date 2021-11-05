from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from rest_framework.decorators import api_view, authentication_classes, permission_classes

import json


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



@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def send_review(request):
    auxiliar = request.data['tabla']
    auxiliar = auxiliar.replace('\\\\u00e1','á')
    auxiliar = auxiliar.replace('\\\\u00e9','é')
    auxiliar = auxiliar.replace('\\\\u00ed','í')
    auxiliar = auxiliar.replace('\\\\u00f3','ó')
    auxiliar = auxiliar.replace('\\\\u00fa','ú')
    auxiliar = auxiliar.replace('\\\\u00f1','ñ')
    auxiliar = auxiliar.replace('?','ñ')
    
    tabla = json.loads(auxiliar)

    for element in tabla:
        if element['estatus_desc'] == 'ACEPTADO':
            element.update({'color':'#D4EFDF'})
        elif element['estatus_desc'] == 'RECHAZADO':
            element.update({'color': '#F2D7D5'})
        elif element['estatus_desc'] == 'EN REVISION':
            element.update({'color': '#F2F3F4'})

    send_email(request,
                {
                    'rfc_provider'  : request.data['rfc'],
                    'tabla'         : tabla
                }, 
                request.data['email'], 
                'Revisión del Padrón de Proveedores UJED', 
                'emails/provider_review.mjml')
    return HttpResponse('terminó review')
