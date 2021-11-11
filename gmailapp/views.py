from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from django.shortcuts import render
from django.http import HttpResponse
import json

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
        'https://www.googleapis.com/auth/admin.directory.user',
    ]
# Create your views here.
def listado(request):
    """Shows basic usage of the Admin SDK Directory API.
    Prints the emails and names of the first 10 users in the domain.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './cadmin/credenciales.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('admin', 'directory_v1', credentials=creds)

    # Call the Admin SDK Directory API
    print('Getting the first 10 users in the domain')
    results = service.users().list(customer='my_customer', maxResults=20,
                                orderBy='email').execute()
    ##resultado = service.groups().list(customer='my_customer').execute()

    users = results.get('users', [])

    if not users:
        print('No users in the domain.')
    else:
        print('Usuarios listado correctamente')


    ##return HttpResponse(u'{0} ({1})'.format("",user['primaryEmail'],
    ##            user['name']['fullName']))

    return render(request, 'inicio.html', {"users":users})


##Vista para eliminar un usuario de la lista de correos
def eliminar(request, usuario):
    #borrar = request.kwargs.get('usuario', None)
    ##borrar = request.get('usuario', None)
    borrar = usuario
    """Shows basic usage of the Admin SDK Directory API.
    Prints the emails and names of the first 10 users in the domain.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './cadmin/credenciales.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('admin', 'directory_v1', credentials=creds)

    # Call the Admin SDK Directory API

    print('Getting the first 10 users in the domain')
    results = service.users().delete(userKey=usuario).execute()

    return HttpResponse("Usuario Eliminado")



 ##Vista para agregar un usuario a la lista de correos


##Vista para Agregar usuarios
def agregar(request):
    """Shows basic usage of the Admin SDK Directory API.
    Prints the emails and names of the first 10 users in the domain.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './cadmin/credenciales.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('admin', 'directory_v1', credentials=creds)
    usuario = {
                "name": {"familyName": "Burtons", "givenName": "Haniels"},
                "password": "some_pass",
                "primaryEmail": "haniels@alumnos.ujed.mx",
                "orgUnitPath": "/alumnos",
            }

    # Call the Admin SDK Directory API
    print('Insercion de datos')
    agregar = service.users().insert(body=usuario).execute()

    return HttpResponse(json.dumps(usuario), content_type='application/json')
