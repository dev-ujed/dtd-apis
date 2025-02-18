from rest_framework import generics, permissions, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.core import serializers, validators
from django.core.exceptions import ValidationError
from django.http import FileResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django.utils.text import slugify

# from social_django.utils import load_strategy, load_backend
# from social_core.backends.oauth import BaseOAuth2
# from social_core.exceptions import MissingBackend, AuthTokenError, AuthForbidden
from requests.exceptions import HTTPError

from .models import *
from .serializers import *

import datetime, time


# Lista los servicios y hace post
class ServiciosListApiView(generics.ListCreateAPIView):
    """
    Inserta y Lista Servicios en el catalogo de Servicios
    """
    authentication_classes  = ()
    permission_classes      = ()
    queryset                = Servicios.objects.all()
    serializer_class        = ServiciosSerializer
    parser_classes          = (FormParser, MultiPartParser)



class SubServicioListApiView(generics.ListCreateAPIView):
    """
    Inserta y Lista SubServicios en el catalogo de SubServicios,
    Requiere como parametro el ID del Servicio
    """
    authentication_classes  = ()
    permission_classes      = ()
    serializer_class        = SubServicioSerializer
    
    def get_queryset(self):
        queryset = Catalogo_SubServicio.objects.filter(servicio_id=self.kwargs["pk"])
        return queryset



class servicioApiView(generics.ListCreateAPIView):
    """
    Inserta y Lista Servicios de la solicitud en la tabla de servicios
    """
    authentication_classes  = ()
    permission_classes      = ()
    queryset                = Servicios.objects.all()
    serializer_class        = servicioSerializer



class subservicioApiView(generics.ListCreateAPIView):
    """
    Inserta y Lista SubServicios de la solicitud en la tabla de subservicios
    """
    authentication_classes  = ()
    permission_classes      = ()
    serializer_class        = subservSerializer
    queryset = SubServicios.objects.raw(
        """
            SELECT solicitudes.solicitudes_subservicios.id, subservicio,solicitudes.solicitudes_catalogo_subservicio.descripcion
            FROM solicitudes.solicitudes_subservicios,solicitudes.solicitudes_catalogo_subservicio
            WHERE solicitudes.solicitudes_subservicios.subservicio::INTEGER=solicitudes.solicitudes_catalogo_subservicio.id::INTEGER
        """
    )



class EstatusViewSet(viewsets.ModelViewSet):
    """
    Genera los metodos de Create o Insert , Updtae y de Listar del Catalogo de Estatus
    """
    authentication_classes  = ()
    permission_classes      = ()
    serializer_class        = EstatusSerializer
    queryset = Catalogo_Estatus.objects.raw(
        """
            SELECT solicitudes.solicitudes_catalogo_estatus.id, key_name, estatus_descrip, tipo_estatus as desc_tipo_estatus
            FROM solicitudes.solicitudes_catalogo_estatus, solicitudes.solicitudes_tipo_estatus 
            WHERE solicitudes.solicitudes_catalogo_estatus.tipo_estatus_id=solicitudes.solicitudes_tipo_estatus.id
            ORDER BY solicitudes.solicitudes_catalogo_estatus.id
        """
    )
    


class UresListApiView(APIView):
    """
    Genera los metodos de Create o Insert y de Listar del Catalogo de Unidades Responsables
    """
    authentication_classes  = ()
    permission_classes      = ()
    # serializer_class      = UnidadesRespSerializer
    def get(self, request, *args, **kwargs):
        ures  = Ures.objects.all().order_by('ures_descrip')
        Querydata = UresSerializer(ures, many=True).data
        UresValue = []
        for ures in Querydata:
            UresList = {}
            UresList.update({ 'key': ures['id'], 'value' : ures['ures_descrip'] })
            UresValue.append(UresList)
        return Response(UresValue)



class EstatusSolicitud(generics.ListAPIView):
    """
    Busca las solicitudes junto con sus archivos y las lista requiere como parametros:
    /estatus/
    """
    authentication_classes  = ()
    permission_classes      = ()
    serializer_class        = SolicitudSerializer
    def get_queryset(self):
        estatus_sol = self.kwargs["estatus"]
        solicitud   = Solicitud.objects.filter(estatus=estatus_sol).order_by('-fecha_sol')
        queryset    = solicitud
        return queryset



class TodasSolicitudes(generics.ListAPIView):
    """
    Consulta todas las solicitudes registradas hasta el momento
    """
    authentication_classes  = ()
    permission_classes      = ()
    serializer_class        = SolicitudSerializer
    def get_queryset(self):
        solicitud = Solicitud.objects.all().order_by('id')
        queryset  = solicitud
        return queryset



class DetalleSolicitud(generics.ListAPIView):
    """
    Busca las solicitudes junto con sus archivos y las lista requiere como parametros:
    /folio/correo
    """
    authentication_classes  = ()
    permission_classes      = ()
    serializer_class        =SolicitudSerializer
    def get_queryset(self):
        folio_sol   = self.kwargs["folio"]
        solicitud   = Solicitud.objects.filter(folio=folio_sol)
        queryset    = solicitud
        return queryset



class DetalleCorreo(generics.ListAPIView):
    """
    Busca las solicitudes junto con sus archivos y las lista requiere como parametros:
    /folio/correo
    """
    authentication_classes  = ()
    permission_classes      = ()
    serializer_class        = SolCorreoSerializer
    def get_queryset(self):
        folio_sol   = self.kwargs["folio"]
        solicitud   = Solicitud.objects.filter(folio=folio_sol)
        queryset    = solicitud
        return queryset



class Tipo_EstatusViewSet(viewsets.ModelViewSet):
    """
    Crud completo para Dashboard_links
    """
    authentication_classes  = ()
    permission_classes      = ()
    queryset                = Tipo_Estatus.objects.all()
    serializer_class        = Tipo_EstatusSerializer



class DetalleServicios(generics.ListAPIView):
    """
    Busca los servicios de las solicitudes junto con sus subservicios y los lista requiere como parametros la llave primaria:
    /pk/
    """
    authentication_classes  = ()
    permission_classes      = ()
    serializer_class        = DetalleServiciosSerializer
    def get_queryset(self):
        id_sol      = self.kwargs["pk"]
        queryset    = Servicios.objects.raw(
            """
       SELECT solicitudes.solicitudes_servicios.id,solicitudes.solicitudes_servicios.solicitud_id,solicitudes.solicitudes_servicios.servicio,solicitudes.solicitudes_catalogo_servicios.descripcion,
(
   select array_to_json(array_agg(row_to_json(t)))
    from (
      select solicitudes.solicitudes_subservicios.id,solicitudes.solicitudes_subservicios.subservicio,solicitudes.solicitudes_catalogo_subservicio.descripcion
        from solicitudes.solicitudes_subservicios,solicitudes.solicitudes_catalogo_subservicio
        where solicitudes.solicitudes_subservicios.subservicio::INTEGER=solicitudes.solicitudes_catalogo_subservicio.id::INTEGER
        and solicitudes.solicitudes_servicios.servicio::INTEGER=solicitudes.solicitudes_subservicios.servicio_id
    ) t
) AS subservicios
       FROM solicitudes.solicitudes_servicios,solicitudes.solicitudes_catalogo_servicios
       where solicitudes.solicitudes_servicios.servicio::INTEGER=solicitudes.solicitudes_catalogo_servicios.id
       and solicitudes.solicitudes_servicios.solicitud_id=%s
           """,
           [id_sol]
)
        return queryset



class MyFileView(APIView):
    """
    Crear y Listar los archivos de las solicitudes
    """
    authentication_classes  = ()
    permission_classes      = ()
    parser_classes          = (MultiPartParser,FormParser)
    # queryset              = MyFile.objects.all()
    # serializer_class      = MyFileSerializer
    def post(self, request, *args, **kwargs):
        solicitud_id   = kwargs.get('pk')
        file           = request.FILES['file']
        nombre_archivo = file.name
        
        if (file.name.endswith('.png') or
            file.name.endswith('.jpeg') or
            file.name.endswith('.gif') or
            file.name.endswith('.bmp') or
            file.name.endswith('.jpg') or
            file.name.endswith('.docx') or
            file.name.endswith('.xlsx') or
            file.name.endswith('.pdf') or
            file.name.endswith('.pptx')):         
            
            data = {
                'file':file,
                'nombre_archivo':nombre_archivo,
                'solicitud':solicitud_id
            }

            file_serializer = MyFileSerializer(data=data)

            if file_serializer.is_valid():
                file_serializer.save()
                return Response(file_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'file':['Archivos permitidos: .jpg, .jpeg, .png, .gif, .bmp, .docx, .xlsx, .pdf, .pptx']},status=422)



class MyFileViewDelete(APIView):
    """
    Eliminar los archivos de las solicitudes requiere como parametro,
    el id del archivo lo lista y lo elimina
    """
    authentication_classes  = ()
    permission_classes      = ()
    parser_classes          = (MultiPartParser,FormParser)
    
    def get(self, request, *args, **kwargs):
        archivo     = get_object_or_404(MyFile, pk=self.kwargs["pk"])
        serializer  = MyFileSerializer(archivo)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        archivo = get_object_or_404(MyFile, pk=self.kwargs["pk"])
        archivo.delete()
        response = {}
        response['success']     = True
        response['message']     = "Archivo eliminado exitosamente"
        response['status']      = status.HTTP_204_NO_CONTENT
        return Response(response)
        #return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        #return Response("Archivo Eliminado", status=status.HTTP_204_NO_CONTENT)



class MyFileViewUpdate(APIView):
    """
    Actualiza los archivos de las solicitudes requiere como parametro,
    el id del archivo lo lista y lo actualiza
    """
    authentication_classes  = ()
    permission_classes      = ()
    parser_classes          = (MultiPartParser,FormParser)

    def get_object(self, pk):
        try:
            return MyFile.objects.get(pk=pk)
        except MyFile.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        archivo     = self.get_object(pk)
        serializer  = MyFileSerializer(archivo)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        archivo     = self.get_object(pk)
        serializer  = MyFileSerializer(archivo, data=request.data)
        if serializer.is_valid():
            sol = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)



class MyFileViewDetails(generics.ListAPIView):
    """
    Busca los archivos y los lista requiere como parametros el id de la solicitud:
    /solicitud_id/
    """
    authentication_classes  = ()
    permission_classes      = ()
    serializer_class        = MyFileSerializer
    def get_queryset(self):
        solicitud_id        = self.kwargs["solicitud_id"]
        queryset = MyFile.objects.raw(
            """
            SELECT * FROM solicitudes.solicitudes_myfile where solicitud_id=%s
            """,
           [solicitud_id]
        )
        return queryset



class SolicitudAPIView(APIView):
    """
    Registra la solicitud de servicio
    """
    authentication_classes  = ()
    permission_classes      = ()

    def post(self,request):
        matricula           = request.data.get("matricula")
        ures                = request.data.get("ures")
        nombre              = request.data.get("nombre")
        apellido_paterno    = request.data.get("apellido_paterno")
        apellido_materno    = request.data.get("apellido_materno")
        correo              = request.data.get("correo")
        extension           = request.data.get("extension")
        telefono            = request.data.get("telefono")
        pautoriza           = request.data.get("pautoriza")
        descripcion         = request.data.get("descripcion")
        estatus_id          = request.data.get("estatus_id")
        area                = request.data.get("area")
        folio               = get_random_string(length=6).upper()
        ures_exists         = (Ures.objects.filter(id=ures))

        if ures_exists:
            ures = request.data.get("ures")
        else:
            return Response({'ures':['La unidad responsable no existe']},status=422)

        #if len(descripcion) > 500:
            #return Response({'errors':'La descripción debe contener maximo 500 caracteres'},status=422)

        def is_email(value):
            try:
               validators.validate_email(value)
               return True
            except validators.ValidationError:
               return False
        email = is_email(correo)
        if(email):
            correo = request.data.get("correo")
        else:
            return Response({'correo':['Su dirección de correo no es valida']},status=422)

        data = {
                'matricula':        matricula,
                'ures':             ures,
                'nombre':           nombre,
                'apellido_paterno': apellido_paterno,
                'apellido_materno': apellido_materno,
                'correo':           correo,
                'extension':        extension,
                'telefono':         telefono,
                'pautoriza':        pautoriza,
                'descripcion':      descripcion,
                'estatus_id':       estatus_id,
                'folio':            folio,
                'area':             area
                #'fecha_sol':       current_time
            }

        serializer = SolicitudSerializer(data=data)
        if serializer.is_valid():
            sol = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)



    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `votes` action.
    """
class SolicitudViewSet(viewsets.ModelViewSet):
    """
    Actualiza o Borra la solicitud de servicio,
    según el verbo que se mande (PUT o DELETE),
    Requiere como parametro el ID de la Solicitud
    """
    authentication_classes  = ()
    permission_classes      = ()
    queryset                = Solicitud.objects.all()
    serializer_class        = SolicitudSerializer



class UpdateTitleRequest(APIView):
    authentication_classes  = ()
    permission_classes      = ()

    def put(self, request, *args, **kwargs):
        folio = kwargs.get('folio')
        solicitud = Solicitud.objects.get(folio=folio)

        data = {
            'titulo' : request.data.get("titulo")
        }
        serializer = SolicitudTituloSerializer(solicitud, data=data)
        if serializer.is_valid():
            sol = serializer.save()
            return Response(serializer.data['titulo'], status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)



class UpdateDescripRequest(APIView):
    authentication_classes  = ()
    permission_classes      = ()

    def get_object(self, pk):
        try:
            return Solicitud.objects.get(pk=pk)
        except Solicitud.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        solicitud   = self.get_object(pk)
        serializer  = SolicitudSerializer(solicitud)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        id          = kwargs.get('pk')
        solicitud   = Solicitud.objects.get(id=id)
        if len(request.data.get("descripcion")) > 500:
            return Response({'descripcion':['La descripción debe contener maximo 500 caracteres']},status=422)
        data = {
            'descripcion' : request.data.get("descripcion")
        }
        serializer = SolicitudDescripcionSerializer(solicitud, data=data)
        if serializer.is_valid():
            sol = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)



class SolicitudUpdateRequest(APIView):
    authentication_classes  = ()
    permission_classes      = ()

    def get_object(self, pk):
        try:
            return Solicitud.objects.get(pk=pk)
        except Participantes.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        solicitud   = self.get_object(pk)
        serializer  = SolicitudUpdateSerializer(solicitud)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        id          = kwargs.get('pk')
        solicitud   = Solicitud.objects.get(id=id)
        descripcion = request.data.get("descripcion")
        def caracter_val(value):
            if len(value) > 500:
                return True
            else:
                return False
        desc        = caracter_val(descripcion)
        if(desc):
            return Response({'descripcion':['La descripción debe contener maximo 500 caracteres']},status=422)
        else:
            descripcion = request.data.get("descripcion")
        data = {
            'matricula':        request.data.get("matricula"),
            'ures':             request.data.get("ures"),
            'nombre':           request.data.get("nombre"),
            'apellido_paterno': request.data.get("apellido_paterno"),
            'apellido_materno': request.data.get("apellido_materno"),
            'correo':           request.data.get("correo"),
            'descripcion':      descripcion,
            'extension':        request.data.get("extension"),
            'telefono':         request.data.get("telefono"),
            'pautoriza':        request.data.get("pautoriza")
        }
        serializer = SolicitudUpdateSerializer(solicitud, data=data)
        if serializer.is_valid():
            sol = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)



class SocialLoginView(generics.GenericAPIView):
     """Log in using facebook"""
     serializer_class       = SocialSerializer
     authentication_classes = ()
     permission_classes     = ()

     def post(self, request):
        """Authenticate user through the provider and access_token"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        provider = serializer.data.get('provider', None)
        strategy = load_strategy(request)

        try:
            backend = load_backend(strategy=strategy, name=provider, redirect_uri=None)
        except MissingBackend:
            return Response({'error': 'Please provide a valid provider'},
            status = status.HTTP_400_BAD_REQUEST)
        
        try:
            if isinstance(backend, BaseOAuth2):
                access_token = serializer.data.get('access_token')
            user = backend.do_auth(access_token)
        except HTTPError as error:
            return Response({
                "error": {
                    "access_token": "Invalid token",
                    "details": str(error)
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        except AuthTokenError as error:
            return Response({
                "error": "Invalid credentials",
                "details": str(error)
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            authenticated_user = backend.do_auth(access_token, user=user)
        except HTTPError as error:
            return Response({
                "error":"invalid token",
                "details": str(error)
            }, status=status.HTTP_400_BAD_REQUEST)
        except AuthForbidden as error:
            return Response({
                "error":"invalid token",
                "details": str(error)
            }, status=status.HTTP_400_BAD_REQUEST)

        if authenticated_user and authenticated_user.is_active:
            #generate JWT token
            login(request, authenticated_user)
            data={
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )}
            #customize the response to your needs
            response = {
                "email":    authenticated_user.email,
                "username": authenticated_user.username,
                "token":    data.get('token')
            }
            return Response(status=status.HTTP_200_OK, data=response)



######################### Users. Menus y Submenus ######################
class RolesViewSet(viewsets.ModelViewSet):
    """
    Crud completo para roles
    """
    authentication_classes  = ()
    permission_classes      = ()
    queryset                = Roles.objects.all()
    serializer_class        = RolesSerializer



class PermissionsViewSet(viewsets.ModelViewSet):
    """
    Crud completo para Permissions
    """
    authentication_classes  = ()
    permission_classes      = ()
    queryset                = Permissions.objects.all()
    serializer_class        = PermissionsSerializer



class Permission_roleViewSet(viewsets.ModelViewSet):
    """
    Crud completo para Permission_role
    """
    authentication_classes  = ()
    permission_classes      = ()
    queryset                = Permission_role.objects.all()
    serializer_class        = Permission_roleSerializer



class Dashboard_sectionsViewSet(viewsets.ModelViewSet):
    """
    Crud completo para Dashboard_sections
    """
    authentication_classes  = ()
    permission_classes      = ()
    queryset                = Dashboard_sections.objects.all()
    serializer_class        = Dashboard_sectionsSerializer



class Dashboard_submenusViewSet(viewsets.ModelViewSet):
    """
    Crud completo para Dashboard_submenus
    """
    authentication_classes  = ()
    permission_classes      = ()
    queryset                = Dashboard_submenus.objects.all()
    serializer_class        = Dashboard_submenusSerializer



class Dashboard_linksViewSet(viewsets.ModelViewSet):
    """
    Crud completo para Dashboard_links
    """
    authentication_classes  = ()
    permission_classes      = ()
    queryset                = Dashboard_links.objects.all()
    serializer_class        = Dashboard_linksSerializer



class UserCreate(APIView):
    authentication_classes  = ()
    permission_classes      = ()
    def post(self,request):
        name        = request.data.get("name")
        last_name   = request.data.get("last_name")
        email       = request.data.get("email")
        active      = request.data.get("active")
        password    = request.data.get("password")
        avatar      = request.data.get("avatar")
        token       = 1
        role        = 1
        data = {
                'name':         name,
                'last_name':    last_name,
                'email':        email,
                'active':       active,
                'password':     password,
                'avatar':       avatar,
                'token':        token,
                'role':         role
            }

        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            sol = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)



class ServicesSub(generics.ListAPIView):
    authentication_classes  = ()
    permission_classes      = ()
    serializer_class        = ServiciosSubSerializer

    def get_queryset(self):
        servicios   = Servicios.objects.all().order_by('descripcion')
        queryset    = servicios
        return queryset



class EstatusProc(APIView):
    authentication_classes  = ()
    permission_classes      = ()

    def get(self, request, *args, **kwargs):
        estatus         = Catalogo_Estatus.objects.filter(tipo_estatus=3).order_by('id')
        Querydata       = EstatusSerializer(estatus, many=True).data
        estatusValue    = []
        for estatus in Querydata:
            estatusList = {}
            estatusList.update({ 'key': estatus['id'], 'value' : estatus['estatus_descrip'] })
            estatusValue.append(estatusList)
        return Response(estatusValue)



class subservicesStore(APIView):
    authentication_classes  = ()
    permission_classes      = ()

    def post(self,request):
        folio           = request.data.get("folio")
        subservice_id   = request.data.get("subservice_id")
        comentario      = request.data.get("comentario")

        UserServicesArrays   = {
            'infraestructura'         : 'jaime.garcia@ujed.mx',
            'desarrollo-de-software'  : 'joseluis.bautista@ujed.mx',
            'cuentas-de-acceso'       : 'alvaro.martinez@ujed.mx',
            'instalacion-de-software' : 'ernesto.cisneros@ujed.mx'
        }

        response        = Solicitud.objects.get(folio=folio)
        solicitud       = SolicitudSerializer(response)
        solicitud_id    = solicitud.data['id']

        status          = Catalogo_Estatus.objects.get(key_name='to-do')
        status_id       = EstatusSerializer(status).data['id']

        status_proc     = Catalogo_Estatus.objects.get(key_name='en-proceso')
        status_proc_id  = EstatusSerializer(status_proc).data['id']

        data = {
            'solicitud':    solicitud_id,
            'estatus':      status_id,
            'subservicio':  subservice_id,
        }

        if comentario != '':
            data.update({ 'comentario' : comentario })

        datasol = {
            'estatus' : status_proc_id
        }

        serializer = subservCreateSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            subservicio     = Catalogo_SubServicio.objects.get(id=subservice_id)
            sub_service     = SubServicioSerializer(subservicio).data
            slug_service    = sub_service['servicio_slug']

            EmailUser       = UserServicesArrays[slug_service]
            user            = Users.objects.get(email=EmailUser)
            user_id         = UserSerializer(user).data['id']

            dataparticipante = {
                'participante' :    user_id,
                'subservicio':      serializer.data['id']
            }

            serialParticiante = ParticipanteSerializer(data=dataparticipante)

            if serialParticiante.is_valid():
                serialParticiante.save()

                subservicioall      = SubServicios.objects.get(id=serializer.data['id'])
                subservicioserial   = subservProcSerializer(subservicioall)
                solicitudSerial     = SolicitudStatusSerializer(response, data=datasol)

                if solicitudSerial.is_valid():
                    solicitudSerial.save()

                    user = request.data.get("user")
                    descripcion='Ha creado el proceso.'
                    current_time = time.strftime(r"%d/%m/%Y %H:%M", time.localtime())

                    dataComment = {
                        'user':             user,
                        'descripcion':      None,
                        'tipo':             'bitacora',
                        'fecha_comment':    current_time,
                        'subservicio':      serializer.data['id']
                    }

                    Commentserializer = ComentariosSerializer(data=dataComment)

                    if Commentserializer.is_valid():
                        Commentserializer.save()

                        dataBitacora = {
                            'user':             user,
                            'descripcion':      descripcion,
                            'comment' :         Commentserializer.data['id'],
                            'fecha_bitacora':   current_time,
                            'subservicio':      serializer.data['id']
                        }

                        Bictacoraserializer = BitacoraSerializer(data=dataBitacora)
                        if Bictacoraserializer.is_valid():
                            Bictacoraserializer.save()

            return Response(subservicioserial.data, status=201)
        else:
            return Response(serializer.errors, status=422)



class UserRol(APIView):
    authentication_classes  = ()
    permission_classes      = ()
    def post(self, request):
        grouplink       = {}
        SubMSection     = {}
        sectionsGroup   = {}
        user_id         = request.data.get("user_id")
        user            = Users.objects.get(id=user_id)
        serializer      = UserSerializer(user)
        rol_id          =  serializer.data['role']
        rol             = Roles.objects.get(id=rol_id)
        rolSerializer   = RolesSerializer(rol)
        permissions     = rolSerializer.data['permissions']
        links           =  Dashboard_links.objects.filter(permission_id__in=permissions).values().order_by('ordered')
        for link in links:
            if link['submenu_id'] in grouplink:
                grouplink[link['submenu_id']].append(link)
            else:
                grouplink.update({link['submenu_id'] : [link]})
        submenuKeys     = grouplink.keys()
        submenus        = Dashboard_submenus.objects.filter(id__in=submenuKeys).values().order_by('ordered')
        for submenu in submenus:
            submenu.update({ 'links': grouplink[submenu['id']] })
            if submenu['section_id'] in SubMSection:
                SubMSection[submenu['section_id']].append(submenu)
            else:
                SubMSection.update({ submenu['section_id'] : [submenu] })
        sectionKeys     = SubMSection.keys()
        sections        = Dashboard_sections.objects.filter(id__in=sectionKeys).values().order_by('ordered')
        i = 0
        for section in sections:
            section.update({ 'submenus': SubMSection[section['id']] })
            sectionsGroup[i] = section
        i+1
        return Response(sectionsGroup)



class LoginView(APIView):
     authentication_classes     = ()
     permission_classes         = ()
     def post(self, request,):
        try:
             email      = request.data.get("email")
             #password  = request.data.get("password")
             user       = Users.objects.get(email=email)
             serializer = UserSerializer(user)
             data =  {'data': serializer.data}
             return Response(data)
        except Users.DoesNotExist:
             return Response({"error": "El usuario no exixte"},status=status.HTTP_400_BAD_REQUEST)



############################################## Participantes ########################################
class ParticipantesAPIView(APIView):
    authentication_classes  = ()
    permission_classes  = ()

    def post(self,request):
        subservicio     = request.data.get("subservicio")
        participante    = request.data.get("participante")
        user            = request.data.get("user")
        current_time    = time.strftime(r"%d/%m/%Y %H:%M", time.localtime())
        participantesQ  = Participantes.objects.filter(subservicio=subservicio).values_list('participante', flat=True)

        if int(participante) in participantesQ:
            return Response({'errors':{ 'participante':'El participante ya está asignado al proceso' }},status=422)

        data = {
            'subservicio':  subservicio,
            'participante': participante
        }

        serializer = ParticipanteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            descripcion = 'Invitó a <strong>'+ serializer.data['participante_name']+' '+serializer.data['participante_last_name']+'</strong> a este servicio.'

            dataComment = {
                'user':         user,
                'descripcion':  None,
                'tipo':         'bitacora',
                'fecha_comment':current_time,
                'subservicio':  subservicio,
            }

            Commentserializer = ComentariosSerializer(data=dataComment)

            if Commentserializer.is_valid():
                Commentserializer.save()

                dataBitacora = {
                    'user':             user,
                    'descripcion':      descripcion,
                    'comment' :         Commentserializer.data['id'],
                    'fecha_bitacora':   current_time,
                    'subservicio':      subservicio,
                }

                Bictacoraserializer = BitacoraSerializer(data=dataBitacora)
                if Bictacoraserializer.is_valid():
                    Bictacoraserializer.save()
                    participanteSave = {}
                    participanteSave.update({'participante': serializer.data})
                    participanteSave.update({ 'bitacora': Bictacoraserializer.data })

            return Response(participanteSave, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def get_object(self, pk):
        try:
            return Participantes.objects.get(pk=pk)
        except Participantes.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        participantes   = self.get_object(pk)
        serializer      = ParticipanteSerializer(participantes)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        id              = kwargs.get('pk')
        participantes   = Participantes.objects.get(id=id)
        #self.get_object(id)
        serializer      = ParticipanteSerializer(participantes, data=request.data)
        if serializer.is_valid():
            sol = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)



class ParticipantesAPIView2(APIView):
    authentication_classes  = ()
    permission_classes      = ()

    def get(self, request, *args, **kwargs):
        query               = Users.objects.all().order_by('id')
        participantes       = GetParticipante(query, many=True).data
        serviciosquiery     = Servicios.objects.all().values('id', 'slug').order_by('id')
        groupServicios      = {}
        for servicio in serviciosquiery:
                groupServicios.update({servicio['slug'] : []})

        for participante in participantes:
            if participante['area_slug'] in groupServicios:
               groupServicios[participante['area_slug']].append(participante)
            else:
                 groupServicios.update({participante['area_slug'] : [participante]})

        return Response(groupServicios)
#######################################################################################################################



################################################# BITACORA Y COMENTARIOS ###############################################
class ComentariosAPIView(APIView):
    authentication_classes  = ()
    permission_classes      = ()

    def post(self,request):
        user            = request.data.get("user")
        descripcion     = request.data.get("descripcion")
        tipo            = request.data.get("tipo")
        subservicio     = request.data.get("subservicio")
        date            = datetime.date.today
        current_time    = time.strftime(r"%d/%m/%Y %H:%M", time.localtime())

        data = {
                'user':             user,
                'descripcion':      descripcion,
                'tipo':             tipo,
                'fecha_comment':    current_time,
                'subservicio':      subservicio,
            }

        serializer = ComentariosSerializer(data=data)
        if serializer.is_valid():
            sol = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def get_object(self, pk):
        try:
            return Comentarios.objects.get(pk=pk)
        except Comentarios.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        comments = self.get_object(pk)
        serializer = ComentariosSerializer(comments)
        return Response(serializer.data)
    
    #def get(self, request, format=None):
        #comments = Comentarios.objects.all()
        #serializer = ComentariosSerializer(comments, many=True)
        #return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        id          = kwargs.get('pk')
        comments    = Comentarios.objects.get(id=id)
        #self.get_object(id)
        serializer  = ComentariosSerializer(comments, data=request.data)
        if serializer.is_valid():
            sol = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)



class BitacoraAPIView(APIView):
    authentication_classes  = ()
    permission_classes      = ()

    def post(self,request):
        user            = request.data.get("user")
        comment         = request.data.get("comment")
        descripcion     = request.data.get("descripcion")
        #date           = datetime.date.today
        current_time    = time.strftime(r"%d/%m/%Y %H:%M", time.localtime())
        #fecha          = date.strftime("%d/%m/%Y %H:%M")
        data = {
            'user':             user,
            'comment':          comment,
            'descripcion':      descripcion,
            'fecha_bitacora':   current_time
            }

        serializer = BitacoraSerializer(data=data)
        if serializer.is_valid():
            sol = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def get_object(self, pk):
        try:
            return Bitacora.objects.get(pk=pk)
        except Bitacora.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        bitacora = self.get_object(pk)
        serializer = BitacoraSerializer(bitacora)
        return Response(serializer.data)

    #def get(self, request, format=None):
        #bitacora = Bitacora.objects.all()
        #serializer = BitacoraSerializer(comments, many=True)
        #return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        id          = kwargs.get('pk')
        bitacora    = Bitacora.objects.get(id=id)
        #self.get_object(id)
        serializer = BitacoraSerializer(bitacora, data=request.data)
        if serializer.is_valid():
            sol = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)



class getFile(APIView):
    authentication_classes  = ()
    permission_classes      = ()

    def get(self, request, *args, **kwargs):
        archivo     = kwargs.get('file')

        file        = open('media/'+archivo, 'rb')
        response    = FileResponse(file)
        return response

class deleteFile(APIView):
    authentication_classes  = ()
    permission_classes      = ()   

    def post(self, request, *args, **kwargs):
        archivo     = kwargs.get('file')
        file        = ('media/'+archivo)
        os.remove(file)
        
    

class ProcesoSolicitud(APIView):
    authentication_classes  = ()
    permission_classes      = ()
    serializer_class        = SolicitudProcesoSerializer

    def get(self, request, *args, **kwargs):
        statusProc      = Catalogo_Estatus.objects.get(key_name='en-proceso')
        status_id       = EstatusSerializer(statusProc).data['id']
        query           = Solicitud.objects.filter(estatus_id=status_id).order_by('-fecha_sol')
        solicitudes     = SolicitudProcesoSerializer(query, many=True).data
        statusquery     = Catalogo_Estatus.objects.filter(desc_tipo_estatus='subservicios').values('key_name').order_by('id')

        for solicitud in solicitudes:
            groupStatus = {}

            for status in statusquery:
                groupStatus.update({status['key_name'] : []})

            for subservicio in solicitud['subservices']:
                if subservicio['estatus_key_name'] in groupStatus:
                    groupStatus[subservicio['estatus_key_name']].append(subservicio)
                else:
                     groupStatus.update({subservicio['estatus_key_name'] : [subservicio]})

            solicitud.update({ 'subservices' : groupStatus })

            for key, value in solicitud['subservices'].items():
                solicitud.update({ 'count_'+slugify(key) : len(value) })

        return Response(solicitudes)



class UpdateSubservice(APIView):
    authentication_classes  = ()
    permission_classes      = ()

    def put(self, request, *args, **kwargs):
        subservice_id   = request.data.get("subservice_id")
        status          = request.data.get('status')
        comentario      = request.data.get("comentario")
        user            = request.data.get("user")

        current_time = time.strftime(r"%d/%m/%Y %H:%M", time.localtime())

        data_subservice = {
            'estatus' : status,
            'estatus_update': current_time
        }

        subservicio             = SubServicios.objects.get(id=subservice_id)
        serializerSubservice    = SubServicioUpdateSerializer(subservicio, data=data_subservice)

        if serializerSubservice.is_valid():
            sol = serializerSubservice.save()

            serializerSubservice = SubServicioGetSerializer(subservicio)

            dataComment = {
                'user':             user,
                'tipo':             'bitacora',
                'fecha_comment':    current_time,
                'subservicio' :     subservice_id
            }

            if comentario == '':
                descripcion = 'Cambió el Estado a <strong>'+serializerSubservice.data['estatus']+'</strong>.'
            else:
                descripcion = 'Cambió el Estado a <strong>'+serializerSubservice.data['estatus']+'</strong> y comentó:'
                dataComment.update({ 'descripcion' : comentario })

            Commentserializer = ComentariosSerializer(data=dataComment)

            if Commentserializer.is_valid():
                Commentserializer.save()

                dataBitacora = {
                    'user':             user,
                    'descripcion':      descripcion,
                    'comment':          Commentserializer.data['id'],
                    'fecha_bitacora':   current_time,
                    'subservicio':      subservice_id
                }

                Bictacoraserializer = BitacoraSerializer(data=dataBitacora)
                if Bictacoraserializer.is_valid():
                    Bictacoraserializer.save()

                    subservicioquery            = Catalogo_SubServicio.objects.get(id=serializerSubservice.data['subservicio_id'])
                    sub_service                 = SubServicioSerializer(subservicioquery).data
                    serializerSubserviceProc    = subservProcSerializer(subservicio)

                    if status == '7':
                        statusquery     = Catalogo_Estatus.objects.filter(desc_tipo_estatus='subservicios').values('key_name').order_by('id')
                        responsesol     = Solicitud.objects.get(id=serializerSubservice.data['solicitud'])
                        solicitud       = SolicitudSerializer(responsesol).data

                        groupStatus = {}
                        for status in statusquery:
                            groupStatus.update({status['key_name'] : []})

                        for subservicio in solicitud['subservices']:
                            if subservicio['estatus_key_name'] in groupStatus:
                                groupStatus[subservicio['estatus_key_name']].append(subservicio)
                            else:
                                 groupStatus.update({subservicio['estatus_key_name'] : [subservicio]})

                        solicitud.update({ 'subservices' : groupStatus })

                        for key, value in solicitud['subservices'].items():
                            solicitud.update({ 'count_'+slugify(key) : len(value) })

                        if int(solicitud['countsubservices']) == int(solicitud['count_concluido']):
                            data = {
                                'estatus':          2,
                                'estatus_update':   current_time,
                            }

                            serializersol = SolicitudStatusSerializer(responsesol, data=data)
                            if serializersol.is_valid():
                                sol             = serializersol.save()
                                subServiceUpate = serializerSubserviceProc.data
                                subServiceUpate.update({'request_finish': True })
                        else:
                            subServiceUpate = serializerSubserviceProc.data
                            subServiceUpate.update({'request_finish': False })
                    else:
                        subServiceUpate = serializerSubserviceProc.data
                        
            return Response(subServiceUpate, status=201)
        else:
            return Response(serializerSubservice.errors, status=422)

