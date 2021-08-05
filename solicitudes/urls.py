from django.urls import path
from rest_framework.routers import DefaultRouter

from .apiviews import *


router=DefaultRouter()

SolicitudEdit = SolicitudViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('sol/roles',                                   RolesViewSet,                       name='roles'),
    path('sol/permissions',                             PermissionsViewSet,                 name='permissions'),
    path('sol/permissions_role',                        Permission_roleViewSet,             name='permissions_role'),
    path('sol/sections',                                Dashboard_sectionsViewSet,          name='sections'),
    path('sol/submenus',                                Dashboard_submenusViewSet,          name='submenus'),
    path('sol/links',                                   Dashboard_linksViewSet,             name='links'),
    path('sol/cat_estatus',                             EstatusViewSet,                     name='estatus'),
    path('sol/tipo_estatus',                            Tipo_EstatusViewSet,                name='tipo_estatus'),

    path('sol/solicitudes/',                            SolicitudAPIView.as_view(),         name='sol_save'),
    path('sol/solicitudes/<int:pk>',                    SolicitudEdit,                      name='sol_edit'),
    path('sol/solicitudes/all/',                        TodasSolicitudes.as_view(),         name='sol_all'),
    path('sol/solicitudes/<int:pk>/upload/',            MyFileView.as_view(),               name='file-upload'),
    path('sol/solicitudes/<int:pk>/update/',            MyFileViewUpdate.as_view(),         name='file-update'),
    path('sol/solicitudes/<int:pk>/delete/',            MyFileViewDelete.as_view(),         name='file-delete'),
    path('sol/solicitudes/<str:solicitud_id>/detalle/', MyFileViewDetails.as_view(),        name='file-detail'),
	path('sol/detallesol/<str:folio>',                  DetalleSolicitud.as_view(),         name='detalle_sol'),
    path('sol/detallecoreo/<str:folio>',                DetalleCorreo.as_view(),            name='detalle_correo'),
    path('sol/estatus_sol/<int:estatus>/',              EstatusSolicitud.as_view(),         name='detalle_sol'),
    path('sol/estatus_proceso/',                        EstatusProc.as_view(),              name='estatus_proc'),
    path('sol/det_servicio/<int:pk>/',                  DetalleServicios.as_view(),         name='detalle_serv'),
	path('sol/cat_servicio/',                           ServiciosListApiView.as_view(),     name='servicio_save'),
	path('sol/cat_servicio/<int:pk>/cat_subservicio/',  SubServicioListApiView.as_view(),   name='subservicio_list'),
    path('sol/servicio/',                               servicioApiView.as_view(),          name='servicio_save'),
    path('sol/subservicio/',                            subservicioApiView.as_view(),       name='subservicio_save'),
	path('sol/ures/',                                   UresListApiView.as_view(),          name='ures_save'),
    path('oauth/login/',                                SocialLoginView.as_view(),          name='login-oauth'),
    path('sol/usuarios/',                               UserCreate.as_view(),               name='usuario_crear'),
    path('sol/usuario-rol/',                            UserRol.as_view(),                  name='usuario_rol'),
    path("sol/login/",                                  LoginView.as_view(),                name="login"),
    path('sol/servicios/',                              ServicesSub.as_view(),              name='servicios_subservicios'),
    path('sol/participantes/',                          ParticipantesAPIView.as_view(),     name='save-participantes'),
    path('sol/participantes/<int:pk>',                  ParticipantesAPIView.as_view(),     name='update-participantes'),
    path('sol/participante/',                           ParticipantesAPIView2.as_view(),    name='get-participantes'),
    path('sol/guardar-subservicio/',                    subservicesStore.as_view(),         name='save-subservices'),
    path('sol/comment/',                                ComentariosAPIView.as_view(),       name='save-comments'),
    path('sol/comment/<int:pk>',                        ComentariosAPIView.as_view(),       name='update-comments'),
    path('sol/bitacora/',                               BitacoraAPIView.as_view(),          name='save-bitacora'),
    path('sol/bitacora/<int:pk>',                       BitacoraAPIView.as_view(),          name='update-bitacora'),
    path('sol/archivo/<str:file>',                      getFile.as_view(),                  name='get_file'),
    path('sol/actualizar-titulo/<str:folio>',           UpdateTitleRequest.as_view(),       name='update_title_request'),
    path('sol/proceso/',                                ProcesoSolicitud.as_view(),         name='proceso-solicitud'),
    path('sol/descripcion/<int:pk>',                    UpdateDescripRequest.as_view(),     name='descrip-solicitud'),
    path('sol/update-sol/<int:pk>',                     SolicitudUpdateRequest.as_view(),   name='update-solicitud'),
    path('sol/actualizar-subservicio/',                 UpdateSubservice.as_view(),         name='update-status'),
]

urlpatterns += router.urls
