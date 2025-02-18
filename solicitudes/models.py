from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models.signals import pre_delete, post_delete
from django.dispatch import receiver
from django.utils.crypto import get_random_string

from .validators import valid_extension,validate_file_size,descripcion_validation,is_email,descripcion_validation_sol

from datetime import datetime
import os


class Tipo_Estatus(models.Model):
    tipo_estatus        = models.CharField(max_length=50, null=True)

    def __str__(self):
        return '{}'.format(self.tipo_estatus)

    class Meta:
        verbose_name_plural = 'Catalogo_Estatus'
        app_label           = 'solicitudes'



class Catalogo_Estatus(models.Model):
    estatus_descrip     = models.CharField(max_length=20, null=True)
    key_name            = models.CharField(max_length=200, null=True, unique=True)
    desc_tipo_estatus   = models.CharField(max_length=200, null=True)
    tipo_estatus        = models.ForeignKey(Tipo_Estatus, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return '{}'.format(self.desc_tipo_estatus,self.key_name,self.tipo_estatus)

    class Meta:
        verbose_name_plural = 'Catalogo_Estatus'
        app_label           = 'solicitudes'



class Servicios(models.Model):
    descripcion         = models.CharField(max_length=200, help_text='Descripción de servicio', null=True, unique=True)
    slug                = models.CharField(max_length=200, help_text='slug de servicio', null=True, unique=True)



class Ures(models.Model):
    ures_ures           = models.CharField(max_length=8)
    ures_descrip        = models.CharField(max_length=300)

    class Meta:
            verbose_name_plural = 'Ures'
            app_label           = 'solicitudes'



class Catalogo_SubServicio(models.Model):
    servicio            = models.ForeignKey('Servicios', related_name='subservicios', on_delete=models.CASCADE)
    descripcion         = models.CharField(max_length=100, help_text='Descripcion de SubServicio', null=True)

    def __str__(self):
        return '{}:{}'.format(self.servicio.description,self.descripcion)

    class Meta:
        verbose_name_plural = 'Catalogo_SubServicio'
        unique_together     = ('servicio','descripcion')
        app_label           = 'solicitudes'



class Solicitud(models.Model):
    titulo              = models.CharField(max_length=40, help_text='Titulo', null=True)
    matricula           = models.CharField(max_length=10, help_text='Matricula', default=None)
    ures                = models.ForeignKey(Ures, on_delete=models.CASCADE, null=True)
    nombre              = models.CharField(max_length=200, help_text='Nombre de quien solicita', default=None)
    apellido_paterno    = models.CharField(max_length=200, help_text='Apellido paterno', default=None)
    apellido_materno    = models.CharField(max_length=200, help_text='Apellido materno', null=True)
    correo              = models.EmailField(max_length=200, help_text='Correo electrónico', null=True, validators=[is_email])
    extension           = models.CharField(max_length=5, help_text='No de Extensión', null=True)
    telefono            = models.CharField(max_length=11, help_text='Telefono de contacto', null=True)
    pautoriza           = models.CharField(max_length=200, help_text='Nombre de quien autoriza', null=True)
    descripcion         = models.CharField(max_length=500, help_text='Descripción de la solicitud', null=True, validators=[descripcion_validation_sol])
    estatus             = models.ForeignKey(Catalogo_Estatus, on_delete=models.CASCADE, null=True)
    folio               = models.CharField(max_length=6, null=True, help_text='Folio generado automaticamente de la solicitud')
    fecha_sol           = models.DateTimeField(auto_now_add=True)
    estatus_update      = models.DateTimeField(null=True)
    area                = models.CharField(max_length=20, null=True)

    def save(self, *args, **kwargs):
        if(self.estatus == None):
            self.estatus = Catalogo_Estatus.objects.get(id = 1)
        super(Solicitud, self).save(*args, **kwargs)

    def __str__(self):
        return '{}:{}:{}:{}:{}:{}:{}:{}:{}:{}:{}:{}'.format(self.matricula,self.ures,self.nombre,self.apellido_paterno,self.apellido_materno,self.correo,
                                          self.extension,self.telefono,self.pautoriza,self.descripcion,self.estatus,self.folio.upper(),self.fecha_sol)

    class Meta:
        verbose_name_plural = 'Solicitud'
        app_label           = 'solicitudes'
        # db_table = 'solicitudes.solicitudes_solicitud'



class MyFile(models.Model):
    solicitud           = models.ForeignKey(Solicitud,on_delete=models.CASCADE, related_name='archivos_solicitud',null=True)
    file                = models.FileField(blank=False, null=True,validators=[valid_extension,validate_file_size])
    descripcion         = models.CharField(max_length=80, null=True,validators=[descripcion_validation,MinLengthValidator(0)])
    nombre_archivo      = models.CharField(max_length=100, null=True)
    subido              = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}:{}'.format(self.file.descripcion,self.subido)

    class Meta:
           verbose_name_plural  = 'MyFile'
           app_label            = 'solicitudes'



@receiver(models.signals.post_delete, sender=MyFile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    '''
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    '''
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)



class SubServicios(models.Model):
    solicitud           = models.ForeignKey(Solicitud, related_name='subservices', on_delete=models.CASCADE, default=None)
    subservicio         = models.ForeignKey(Catalogo_SubServicio, related_name='subservicio', on_delete=models.CASCADE, default=None)
    estatus             = models.ForeignKey(Catalogo_Estatus, related_name='status', on_delete=models.CASCADE, null=True)
    fec_subservicio     = models.DateTimeField(auto_now_add=True, null=True)
    estatus_update      = models.DateTimeField(null=True)
    comentario          = models.CharField(max_length=150, null=True)

    class Meta:
           verbose_name_plural='subservicios'
           app_label='solicitudes'



class DetalleSolicitud(models.Model):
    id                  = models.IntegerField(primary_key=True)
    titulo              = models.CharField(max_length=40, help_text='Titulo', null=True)
    matricula           = models.CharField(max_length=10, help_text='Matricula', default=None)
    ures                = models.ForeignKey(Ures, on_delete=models.CASCADE, null=True)
    nombre              = models.CharField(max_length=200, help_text='Nombre de quien solicita', default=None)
    apellido_paterno    = models.CharField(max_length=200, help_text='Apellido paterno', default=None)
    apellido_materno    = models.CharField(max_length=200, help_text='Apellido materno', null=True)
    correo              = models.EmailField(max_length=200, help_text='Correo electrónico', default=None)
    extension           = models.CharField(max_length=5, help_text='No de Extensión', null=True)
    telefono            = models.CharField(max_length=11, help_text='Telefono de contacto', null=True)
    pautoriza           = models.CharField(max_length=200, help_text='Nombre de quien autoriza', null=True)
    descripcion         = models.CharField(max_length=500, help_text='Descripción de la solicitud', null=True)
    estatus             = models.ForeignKey(Catalogo_Estatus, on_delete=models.CASCADE, null=True)
    folio               = models.CharField(max_length=6, null=True, help_text='Folio generado automaticamente de la solicitud')
    fecha_sol           = models.DateTimeField(auto_now_add=True)
    servicios           = models.ManyToManyField('Servicios', related_name='servicio')
    # subservices         = models.ManyToManyField(Catalogo_SubServicio, through='subServicios')
    # archivos            = models.ForeignKey(MyFile,on_delete=models.CASCADE,null=True)
    
    
    def __str__(self):
        return '{}:{}:{}:{}:{}:{}:{}:{}:{}:{}:{}:{}'.format(self.matricula,self.ures,self.nombre,self.apellido_paterno,self.apellido_materno,
                                                            self.correo,self.extension,self.telefono,self.pautoriza,self.descripcion,self.estatus,
                                                            self.folio.upper(),self.fecha_sol)

    class Meta:
        managed             = False
        app_label           = 'solicitudes'
        verbose_name_plural = 'DetalleSolicitud'
        #db_table = 'solicitudes.solicitudes_solicitud'



class DetalleServicios(models.Model):
    id                  = models.IntegerField(primary_key=True)
    solicitud_id        = models.IntegerField()
    servicio            = models.IntegerField()
    descripcion         = models.CharField(max_length=500, null=True)
    subservicios        = ArrayField(models.CharField(max_length=500), blank=True)



#############################Tablas de Usuarios###################################
class Permissions(models.Model):
    id                  = models.IntegerField(primary_key=True)
    key_name            = models.CharField(max_length=200, null=True, unique=True)
    name                = models.CharField(max_length=200, null=True)
    date                = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.id,self.key_name,self.name,self.date)

    class Meta:
        verbose_name_plural = 'Permissions'
        app_label           = 'solicitudes'



class Roles(models.Model):
    id                  = models.IntegerField(primary_key=True)
    key_name            = models.CharField(max_length=200, null=True, unique=True)
    name                = models.CharField(max_length=200, null=True)
    date                = models.DateTimeField(auto_now_add=True)
    permissions         = models.ManyToManyField(Permissions, through='Permission_role')

    def __str__(self):
        return '{}'.format(self.id,self.key_name,self.date)

    class Meta:
        verbose_name_plural = 'Roles'
        app_label           = 'solicitudes'



class Permission_role(models.Model):
    permissions         = models.ForeignKey(Permissions, related_name='permission', on_delete=models.CASCADE, default=None)
    role                = models.ForeignKey(Roles, related_name='role', on_delete=models.CASCADE, default=None)

    def __str__(self):
        return '{}'.format(self.permissions,self.role)

    class Meta:
        verbose_name_plural = 'Permission_role'
        unique_together     = ('permissions','role')
        app_label           = 'solicitudes'



class Users(models.Model):
    name                = models.CharField(max_length=100, null=True)
    last_name           = models.CharField(max_length=100, null=True)
    email               = models.CharField(max_length=200, null=True, unique=True)
    active              = models.BooleanField()
    password            = models.CharField(max_length=300, default=None)
    avatar              = models.CharField(max_length=60, null=True)
    token               = models.IntegerField()
    role                = models.ForeignKey(Roles,related_name='role_id',on_delete=models.CASCADE,default=None)
    date                = models.DateTimeField(auto_now_add=True)
    area                = models.ForeignKey(Servicios,related_name='area_serv',on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return '{}'.format(self.id,self.name,self.last_name,self.email,self.active,self.password,self.avatar,
                            self.role_id,self.token,self.role,self.date)

    class Meta:
        verbose_name_plural = 'Users'
        app_label           = 'solicitudes'



############################## Tablas para menus y Sub menus #####################
class Dashboard_sections(models.Model):
    name                = models.CharField(max_length=20, null=True, unique=True)
    title               = models.CharField(max_length=50, null=True)
    ordered             = models.IntegerField(null=True)
    date                = models.DateTimeField(auto_now_add=True)
    active              = models.IntegerField(null=True)
    slug                = models.CharField(max_length=100, null=True)



class Dashboard_submenus(models.Model):
    name                = models.CharField(max_length=20, null=True)
    icon                = models.CharField(max_length=50, null=True)
    active              = models.IntegerField(null=True)
    searchable_name     = models.CharField(max_length=100, null=True)
    ordered             = models.IntegerField()
    date                = models.DateTimeField(auto_now_add=True)
    section             = models.ForeignKey(Dashboard_sections, related_name='section', on_delete=models.CASCADE, default=None)

    class Meta:
        verbose_name_plural = 'dashboard_submenus'
        unique_together     = ('name','section')
        app_label           = 'solicitudes'



class Dashboard_links(models.Model):
    name                = models.CharField(max_length=60, null=True)
    route               = models.CharField(max_length=200, null=True)
    ordered             = models.IntegerField()
    date                = models.DateTimeField(auto_now_add=True)
    active              = models.IntegerField(null=True)
    submenu             = models.ForeignKey(Dashboard_submenus, related_name='submenu_id', on_delete=models.CASCADE, default=None)
    permission          = models.ForeignKey(Permissions, related_name='permission_id', on_delete=models.CASCADE, default=None)

    class Meta:
        verbose_name_plural = 'dashboard_links'
        unique_together     = ('name','submenu')
        app_label           = 'solicitudes'
#####################################################################################################################



##################################### participantes #################################################################
class Participantes(models.Model):
    subservicio         = models.ForeignKey(SubServicios, related_name='sub_servicioParticipantes', on_delete=models.CASCADE, default=None)
    participante        = models.ForeignKey(Users, related_name='participante', on_delete=models.CASCADE, default=None)

    def __str__(self):
        return '{}'.format(self.subservicio,self.participante)

    class Meta:
        verbose_name_plural = 'Participantes'
        app_label           = 'solicitudes'
#######################################################################################################################



################################################# BITACORA Y COMENTARIOS ###############################################
class Comentarios(models.Model):
    user                = models.ForeignKey(Users, related_name='user_coment', on_delete=models.CASCADE, default=None)
    subservicio         = models.ForeignKey(SubServicios, related_name='sub_serviciocomentario', on_delete=models.CASCADE, default=None)
    fecha_comment       = models.DateTimeField(auto_now_add=True)
    descripcion         = models.CharField(max_length=150, null=True, default='')
    tipo                = models.CharField(max_length=20, null=True)
    
    def __str__(self):
        return '{}'.format(self.subservicio,self.participante)
    
    class Meta:
        verbose_name_plural='Comentarios'
        app_label='solicitudes'



class Bitacora(models.Model):
    user                = models.ForeignKey(Users, related_name='user_bit', on_delete=models.CASCADE, default=None)
    subservicio         = models.ForeignKey(SubServicios, related_name='sub_serviciobit', on_delete=models.CASCADE, default=None)
    comment             = models.ForeignKey(Comentarios, related_name='comment_bit', on_delete=models.CASCADE, default=None)
    descripcion         = models.CharField(max_length=150, null=True)
    fecha_bitacora      = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return '{}'.format(self.subservicio,self.participante)
    
    class Meta:
        verbose_name_plural = 'Bitacora'
        app_label           = 'solicitudes'

class BitacoraServicios(models.Model):
    unidad = models.CharField(max_length=40)
    folio_sistema = models.CharField(max_length=40)
    solicitado_por = models.CharField(max_length=40)
    folio_interno = models.CharField(max_length=40)
    fecha = models.DateField(auto_now_add=True)
    solicitud = models.CharField(max_length=200)
    diagnostico = models.CharField(max_length=200)
    material = models.CharField(max_length=200)