from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.inicio, name='inicio'),
    path('login/', views.login_views, name='login_views'),
    path('inicio/', views.inicio, name='inicio'),
    path('inicio-admin/', views.inicio_admin, name='inicio_admin'),
    path('inicio-usuario/', views.inicio_usuario, name='inicio_usuario'),
    #CLASE
    path('nuevaClase/',views.nuevaClase, name='nuevaClase'),
    path('listadoClase/',views.listadoClase, name='listadoClase'),
    path('guardarClase/',views.guardarClase, name='guardarClase'),
    path('eliminarClase/<id_clase>',views.eliminarClase),
    path('editarClase/<id_clase>',views.editarClase),
    path('procesarEdicionClase/',views.procesarEdicionClase, name='procesarEdicionClase'),
    #MATERIAL
    path('nuevoMaterial/',views.nuevoMaterial, name='nuevoMaterial'),
    path('listadoMaterial/',views.listadoMaterial, name='listadoMaterial'),
    path('guardarMaterial/',views.guardarMaterial, name='guardarMaterial'),
    path('eliminarMaterial/<id_material>',views.eliminarMaterial),
    path('editarMaterial/<id_material>',views.editarMaterial),
    path('procesarEdicionMaterial/',views.procesarEdicionMaterial, name='procesarEdicionMaterial'),
    #TAREA
    path('nuevaTarea/',views.nuevaTarea, name='nuevaTarea'),
    path('listadoTarea/',views.listadoTarea, name='listadoTarea'),
    path('guardarTarea/',views.guardarTarea, name='guardarTarea'),
    path('eliminarTarea/<id_tarea>',views.eliminarTarea),
    path('editarTarea/<id_tarea>',views.editarTarea),
    path('procesarEdicionTarea/',views.procesarEdicionTarea, name='procesarEdicionTarea'),
    path('subirTarea/',views.subirTarea, name='subirTarea'),
    path('listadoSubida/',views.listadoSubida, name='listadoSubida'),
    path('guardarEntrega/',views.guardarEntrega, name='guardarEntrega'),
    #RETROALIMENTACION
    path('nuevoComentario/',views.nuevoComentario, name='nuevoComentario'),
    path('listadoComentario/',views.listadoComentario, name='listadoComentario'),
    path('guardarComentario/',views.guardarComentario, name='guardarComentario'),
    path('eliminarComentario/<id_retro>',views.eliminarComentario),
    path('editarComentario/<id_retro>',views.editarComentario),
    path('procesarEdicionComentario/',views.procesarEdicionComentario, name='procesarEdicionComentario'),


 
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
