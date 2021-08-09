from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils.text import slugify

from .models import *
import datetime, os


class SubServicioServSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalogo_SubServicio
        fields = ('id', 'descripcion')



class ServiciosSubSerializer(serializers.ModelSerializer):
    subservicios            = serializers.SerializerMethodField()

    def get_subservicios(self, instance):
        subservices = instance.subservicios.all().order_by('descripcion')
        subs = SubServicioServSerializer(subservices, many=True).data
        subserviciosValue = []
        for subservicio in subs:
            subservicios = {}
            subservicios.update({ 'key': subservicio['id'], 'value' : subservicio['descripcion'] })
            subserviciosValue.append(subservicios)
        return subserviciosValue

    class Meta:
        model = Servicios
        fields = ('descripcion', 'slug', 'subservicios')



class ServiciosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicios
        fields = '__all__'



class servicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicios
        fields = '__all__'



class SubServicioSerializer(serializers.ModelSerializer):
    servicio                = serializers.CharField(source='servicio.descripcion', read_only=True)
    servicio_slug           = serializers.CharField(source='servicio.slug', read_only=True)
    
    class Meta:
        model = Catalogo_SubServicio
        fields = '__all__'



class SubServicioUpdateSerializer(serializers.ModelSerializer):
    estatus_update          = serializers.DateTimeField(format="%d/%m/%Y %H:%M", input_formats=['%d/%m/%Y %H:%M','iso-8601'], required=False)
    
    class Meta:
        model = SubServicios
        fields = '__all__'



class SubServicioGetSerializer(serializers.ModelSerializer):
    subservicio             = serializers.CharField(source='subservicio.descripcion', read_only=True)
    subservicio_id          = serializers.CharField(source='subservicio.id', read_only=True)
    servicio                = serializers.CharField(source='subservicio.servicio.descripcion', read_only=True)
    servicios_slug          = serializers.CharField(source='subservicio.servicio.slug', read_only=True)
    fec_subservicio         = serializers.DateTimeField(format="%d/%m/%Y %H:%M", input_formats=['%d/%m/%Y %H:%M','iso-8601'], read_only=True)
    estatus_update          = serializers.DateTimeField(format="%d/%m/%Y %H:%M", input_formats=['%d/%m/%Y %H:%M','iso-8601'], read_only=True, required=False)
    estatus                 = serializers.CharField(source='estatus.estatus_descrip', read_only=True)
    estatus_slug            = serializers.CharField(source='estatus.key_name', read_only=True)
    estatus_id              = serializers.CharField(source='estatus.id', read_only=True)

    class Meta:
        model = SubServicios
        fields = '__all__'



class subservSerializer(serializers.ModelSerializer):
    subservicio             = serializers.CharField(source='subservicio.descripcion', read_only=True)
    servicio                = serializers.CharField(source='subservicio.servicio.descripcion', read_only=True)
    id                      = serializers.CharField(source='subservicio.id', read_only=True)
    fec_subservicio         = serializers.DateTimeField(format="%d/%m/%Y %H:%M", input_formats=['%d/%m/%Y %H:%M','iso-8601'])
    estatus_update          = serializers.DateTimeField(format="%d/%m/%Y %H:%M", input_formats=['%d/%m/%Y %H:%M','iso-8601'])
    estatus                 = serializers.CharField(source='estatus.estatus_descrip', read_only=True)
    servicio_slug           = serializers.CharField(source='subservicio.servicio.slug', read_only=True)

    class Meta:
        model = SubServicios
        fields = '__all__'



class GetParticipante(serializers.ModelSerializer):
    area                    = serializers.CharField(source='area.descripcion', read_only=True)
    area_slug               = serializers.CharField(source='area.slug', read_only=True)
    searchable_name         = serializers.SerializerMethodField()

    def get_searchable_name(self, obj):
        complete_name = f'{obj.name} {obj.last_name}'
        return slugify(complete_name)

    class Meta:
        model=Users
        fields = ('id','name','last_name','avatar', 'area','area_slug', 'searchable_name')



class ParticipanteSerializer(serializers.ModelSerializer):
    id                      = serializers.CharField(source='participante.id', read_only=True)
    participante_name       = serializers.CharField(source='participante.name', read_only=True)
    participante_last_name  = serializers.CharField(source='participante.last_name', read_only=True)
    searchable_name         = serializers.SerializerMethodField()
    participante_avatar     = serializers.CharField(source='participante.avatar', read_only=True)
    area                    = serializers.CharField(source='participante.area.descripcion', read_only=True)
    subservicio_descrip     = serializers.CharField(source='subservicio.subservicio.descripcion', read_only=True)
    # subservices             = subservProcSerializer(read_only=True, many=True)

    def get_searchable_name(self, obj):
        complete_name = f'{obj.participante.name} {obj.participante.last_name}'
        return slugify(complete_name)

    class Meta:
        model=Participantes
        fields = '__all__'

        def create(self, validated_data):
            participantes = Participantes(
                subservicio = validated_data['subservicio'],
                participante  = validated_data['participante'],
            )
            participantes.save()
            return participantes



class ParticipanteProcSerializer(serializers.ModelSerializer):
    participante_name       = serializers.CharField(source='participante.name', read_only=True)
    id                      = serializers.CharField(source='participante.id', read_only=True)
    participante_last_name  = serializers.CharField(source='participante.last_name', read_only=True)
    participante_avatar     = serializers.CharField(source='participante.avatar', read_only=True)

    class Meta:
        model=Participantes
        fields = ('id', 'participante_avatar', 'participante_name', 'participante_last_name')



class subservCreateSerializer(serializers.ModelSerializer):
    subservicio_name        = serializers.CharField(source='subservicio.descripcion' ,read_only=True)
    servicio                = serializers.CharField(source='subservicio.servicio.descripcion', read_only=True)
    fec_subservicio         = serializers.DateTimeField(default=None, format="%d/%m/%Y %H:%M", input_formats=['%d/%m/%Y %H:%M','iso-8601'])
    estatus_update          = serializers.DateTimeField(default=None, format="%d/%m/%Y %H:%M", input_formats=['%d/%m/%Y %H:%M','iso-8601'])
    estatus_name            = serializers.CharField(source='estatus.estatus_descrip', read_only=True)
    comentario              = serializers.CharField(default=None)
    servicios_slug          = serializers.CharField(source='subservicio.servicio.slug', read_only=True)

    class Meta:
        model=SubServicios
        fields = '__all__'

    def create(self, validated_data):
        subservicios = SubServicios(
            solicitud   = validated_data['solicitud'],
            subservicio = validated_data['subservicio'],
            comentario  = validated_data['comentario'],
            estatus     = validated_data['estatus'],
        )
        subservicios.save()
        return subservicios



class ComentariosProcSerializer(serializers.ModelSerializer):
    fecha_comment           = serializers.DateTimeField(format="%d/%m/%Y %H:%M", input_formats=['%d/%m/%Y %H:%M','iso-8601'],required=False)
    user_avatar             = serializers.CharField(source='user.avatar', read_only=True)
    user_name               = serializers.CharField(source='user.name', read_only=True)
    user_last_name          = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        model = Comentarios
        fields = '__all__'



class BitacoraProcSerializer(serializers.ModelSerializer):
    fecha_bitacora          = serializers.DateTimeField(format="%d/%m/%Y %H:%M", input_formats=['%d/%m/%Y %H:%M','iso-8601'],required=False)
    user_avatar             = serializers.CharField(source='user.avatar', read_only=True)
    user_name               = serializers.CharField(source='user.name', read_only=True)
    user_last_name          = serializers.CharField(source='user.last_name', read_only=True)
    comentario              = serializers.CharField(source='comment.descripcion', read_only=True)
    fecha_comment           = serializers.DateTimeField(source='comment.fecha_comment', format="%d/%m/%Y %H:%M",read_only=True)

    class Meta:
        model = Bitacora
        fields = '__all__'



class subservProcSerializer(serializers.ModelSerializer):
    subservicio_name        = serializers.CharField(source='subservicio.descripcion' ,read_only=True)
    servicio                = serializers.CharField(source='subservicio.servicio.descripcion', read_only=True)
    fec_subservicio         = serializers.DateTimeField(default=None, format="%d/%m/%Y %H:%M", input_formats=['%d/%m/%Y %H:%M','iso-8601'])
    estatus_update          = serializers.DateTimeField(default=None, format="%d/%m/%Y %H:%M", input_formats=['%d/%m/%Y %H:%M','iso-8601'])
    estatus_name            = serializers.CharField(source='estatus.estatus_descrip', read_only=True)
    estatus_key_name        = serializers.CharField(source='estatus.key_name', read_only=True)
    servicios_slug          = serializers.CharField(source='subservicio.servicio.slug', read_only=True)
    sub_servicioParticipantes = ParticipanteProcSerializer(read_only=True, many=True)
    solicitud_folio         = serializers.CharField(source='solicitud.folio', read_only=True)
    comentarios_publicos    = serializers.SerializerMethodField()
    comentarios_privados    = serializers.SerializerMethodField()
    bitacora                = serializers.SerializerMethodField()

    def get_comentarios_publicos(self, instance):
        query = instance.sub_serviciocomentario.filter(tipo='publico').order_by('-fecha_comment')
        comments = ComentariosProcSerializer(query, many=True).data
        return comments

    def get_comentarios_privados(self, instance):
        query = instance.sub_serviciocomentario.filter(tipo='privado').order_by('-fecha_comment')
        comments = ComentariosProcSerializer(query, many=True).data
        return comments

    def get_bitacora(self, instance):
        query = instance.sub_serviciobit.all().order_by('-fecha_bitacora')
        bitacora = BitacoraProcSerializer(query, many=True).data
        return bitacora

    class Meta:
        model = SubServicios
        fields = '__all__'



class EstatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalogo_Estatus
        fields = '__all__'



class Tipo_EstatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo_Estatus
        fields = '__all__'



class MyFileSerializer(serializers.ModelSerializer):
    subido                  = serializers.DateTimeField(format="%d/%m/%Y %H:%M", input_formats=['%d/%m/%Y %H:%M','iso-8601'],required=False)
    urlfile                 = serializers.SerializerMethodField()
    sizefile                = serializers.SerializerMethodField()
    
    def get_sizefile(self, obj):
        path = 'media/'+str(obj.file)
        size = os.path.getsize(path)
        return size
    
    def get_urlfile(self, obj):
        storage_location = 'http://192.168.10.46/solicitudes/sol/archivo'
        img_url = f'{storage_location}/{obj.file}'
        return img_url
    
    class Meta:
        model=MyFile
        fields = '__all__'



class SolicitudProcesoSerializer(serializers.ModelSerializer):
    subservices             = subservProcSerializer(read_only=True, many=True)
    countsubservices        = serializers.IntegerField(source='subservices.count', read_only=True)
    ures_desc               = serializers.CharField(source='ures.ures_descrip', read_only=True)
    count_archivos          = serializers.IntegerField(source='archivos_solicitud.count', read_only=True)
    fecha_sol               = serializers.DateTimeField(format="%d/%m/%Y %H:%M", input_formats=['%d/%m/%Y %H:%M','iso-8601'])
    estatus                 = serializers.CharField(source='estatus.estatus_descrip', read_only=True)

    class Meta:
        model = Solicitud
        fields = ('id','folio', 'titulo', 'nombre', 'apellido_paterno', 'apellido_materno', 'fecha_sol', 'estatus','count_archivos', 'ures','ures_desc','countsubservices', 'subservices')



class SolicitudSerializer(serializers.ModelSerializer):
    subservices             = subservProcSerializer(read_only=True, many=True)
    countsubservices        = serializers.IntegerField(source='subservices.count', read_only=True)
    estatus_desc            = serializers.CharField(source='estatus.estatus_descrip', read_only=True)
    ures_desc               = serializers.CharField(source='ures.ures_descrip', read_only=True)
    archivos_solicitud      = MyFileSerializer(read_only=True,many=True)
    count_archivos          = serializers.IntegerField(source='archivos_solicitud.count', read_only=True)
    fecha_sol               = serializers.DateTimeField(default=None, format="%d/%m/%Y %H:%M", input_formats=['%d/%m/%Y %H:%M','iso-8601'],required=False)

    class Meta:
        model = Solicitud
        fields = '__all__'



class SolicitudTituloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitud
        fields = ('id', 'titulo')

    def create(self, validated_data):
        solicitud = Solicitud(
            titulo = validated_data['titulo']
        )
        solicitud.save()
        return solicitud



class SolicitudDescripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitud
        fields = ('id', 'descripcion','nombre','correo','folio')

    def create(self, validated_data):
        solicitud = Solicitud(
            descripcion = validated_data['descripcion']
        )
        solicitud.save()
        return solicitud



class SolicitudUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitud
        fields = ('id','matricula','ures','nombre','apellido_paterno','apellido_materno', 'correo','extension','telefono','pautoriza','folio')

    def create(self, validated_data):
        solicitud = Solicitud(
            matricula           = validated_data['matricula'],
            ures                = validated_data['ures'],
            nombre              = validated_data['nombre'],
            apellido_paterno    = validated_data['apellido_paterno'],
            apellido_materno    = validated_data['apellido_materno'],
            correo              = validated_data['correo'],
            extension           = validated_data['extension'],
            telefono            = validated_data['telefono'],
            pautoriza           = validated_data['pautoriza']
        )
        solicitud.save()
        return solicitud



class SolicitudStatusSerializer(serializers.ModelSerializer):
    estatus_update          = serializers.DateTimeField(required=False, format="%d/%m/%Y %H:%M", input_formats=['%d/%m/%Y %H:%M','iso-8601'])
    
    class Meta:
        model = Solicitud
        fields = '__all__'

    def create(self, validated_data):
        solicitud = Solicitud(
            estatus = validated_data['estatus'],
            estatus_update = validated_data['estatus_update'],
        )
        solicitud.save()
        return solicitud



class DetalleSolicitudSerializer(serializers.ModelSerializer):
    subservices             = subservSerializer(read_only=True, many=True)
    countsubservices        = serializers.IntegerField(source='subservices.count', read_only=True)
    estatus                 = serializers.CharField(source='estatus.Descripcion', read_only=True)
    ures                    = serializers.CharField(source='ures.ures_descrip', read_only=True)
    archivos                = MyFileSerializer(read_only=True, many=True)
    countarchivos           = serializers.IntegerField(source='archivos.count', read_only=True)
    
    class Meta:
        model = Solicitud
        fields = '__all__'



class subservCorreoSerializer(serializers.ModelSerializer):
    subservicio_name        = serializers.CharField(source='subservicio.descripcion' ,read_only=True)
    estatus_key_name        = serializers.CharField(source='estatus.key_name', read_only=True)

    class Meta:
        model = SubServicios
        fields = ('subservicio_name','estatus_key_name')



class SolCorreoSerializer(serializers.ModelSerializer):
    subservices             = subservCorreoSerializer(read_only=True, many=True)

    class Meta:
        model = Solicitud
        fields = ('id','correo','subservices')



class DetalleServiciosSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleServicios
        fields = '__all__'



class UresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ures
        fields = '__all__'



class UnidadesRespSerializer(serializers.ModelSerializer):
    unidades                = serializers.SerializerMethodField()
    
    def get_subservicios(self, instance):
        escuelas = instance.unidades.all().order_by('ures_descrip')
        ures = UresSerializer(escuelas, many=True).data
        unidades = {}
        for x in ures:
            unidades.update({ x['id']: x['ures_descrip']})
        return unidades
    
    class Meta:
        model = Ures
        fields = ('id', 'ures_descrip')



class SocialSerializer(serializers.Serializer):
    """
    Serializer which accepts an OAuth2 access token and provider.
    """
    provider                = serializers.CharField(max_length=255, required=True)
    access_token            = serializers.CharField(max_length=4096, required=True, trim_whitespace=True)



############################# Serializers para Usuarios, Menus y Submenus####################################
class PermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permissions
        fields = '__all__'



class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = '__all__'



class Permission_roleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission_role
        fields = '__all__'



class Dashboard_sectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dashboard_sections
        fields = '__all__'



class Dashboard_submenusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dashboard_submenus
        fields = '__all__'



class Dashboard_linksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dashboard_links
        fields = '__all__'



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'

    def create(self, validated_data):
        user = Users(
                name        = validated_data['name'],
                last_name   = validated_data['last_name'],
                email       = validated_data['email'],
                active      = validated_data['active'],
                password    = validated_data['password'],
                avatar      = validated_data['avatar'],
                token       = validated_data['token'],
                role        = validated_data['role']
            )
        #user.set_password(validated_data['password'])
        user.save()
        #Token.objects.create(user=user)
        return user
#######################################################################################################################



################################################# BITACORA Y COMENTARIOS ###############################################
class ComentariosSerializer(serializers.ModelSerializer):
    fecha_comment           = serializers.DateTimeField(format="%d/%m/%Y %H:%M", input_formats=['%d/%m/%Y %H:%M','iso-8601'], required=False)
    user_name               = serializers.CharField(source='user.name', read_only=True)
    user_last_name          = serializers.CharField(source='user.last_name', read_only=True)
    
    class Meta:
        model = Comentarios
        fields = '__all__'



class BitacoraSerializer(serializers.ModelSerializer):
    fecha_bitacora          = serializers.DateTimeField(format="%d/%m/%Y %H:%M", input_formats=['%d/%m/%Y %H:%M','iso-8601'], required=False)
    user_avatar             = serializers.CharField(source='user.avatar', read_only=True)
    user_name               = serializers.CharField(source='user.name', read_only=True)
    user_last_name          = serializers.CharField(source='user.last_name', read_only=True)
    comentario              = serializers.CharField(source='comment.descripcion', read_only=True)
    fecha_comment           = serializers.DateTimeField(source='comment.fecha_comment', format="%d/%m/%Y %H:%M", read_only=True)

    class Meta:
        model = Bitacora
        fields = '__all__'
