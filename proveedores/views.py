from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string


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



def send_password(request, email_provider, rfc_provider, pass_provider):
    print(email_provider, rfc_provider, pass_provider)
    send_email(request,
                {
                    'rfc_provider'      : rfc_provider,
                    'pass_provider'     : pass_provider
                }, 
                email_provider, 
                'Activación de Usuario del Padrón de Proveedores UJED', 
                'emails/provider_password.mjml')
    return HttpResponse('terminó')
