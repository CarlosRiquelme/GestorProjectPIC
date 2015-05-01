from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'GestorProjectPIC.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^reset/password_reset/$', 'django.contrib.auth.views.password_reset', name='admin_password_reset'),
    url(r'^reset/password_reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', name='password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),
    url(r'^accounts/login/', include(admin.site.urls) , name='login'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # url(r'^user_story/crear', 'PIC.views.crear_user_story'),

#USUARIOS



    url(r'^usuario/nuevo/$', 'PIC.views.nuevo_usuario'),
    url(r'^usuarios/$','PIC.views.usuarios'),
    url(r'^usuario/eliminar/(?P<id_user>\d+)/$','PIC.views.desactivar_usuario'),
    url(r'^usuario/activar/(?P<id_user>\d+)/$','PIC.views.activar_usuario'),
    url(r'^usuario/editar/(?P<id_user>\d+)/$','PIC.views.editar_usuario'),



#PROYECTO
     url(r'^proyecto/nuevo$','AdminProyectos.views.nuevo_proyecto'),
     url(r'^proyectos/$', 'AdminProyectos.views.proyectos'),
     url(r'^proyecto/editar/(?P<id_proyecto>\d+)/$','AdminProyectos.views.editar_proyecto'),
     url(r'^proyecto/iniciar/(?P<id_proyecto>\d+)/$','AdminProyectos.views.iniciar_proyecto'),
     url(r'^proyecto/eliminar/(?P<id_proyecto>\d+)/$','AdminProyectos.views.eliminar_proyecto'),
     url(r'^proyecto/misproyectos/$','AdminProyectos.views.mis_proyectos'),
     url(r'^proyecto/miproyecto/(?P<id_proyecto>\d+)/$','AdminProyectos.views.mi_proyecto'),
     url(r'^proyecto/colaboradores/(?P<id_proyecto>\d+)/$','AdminProyectos.views.colaboradores'),


#ROLES

    url(r'^rol/listar/$', 'PIC.views.roles', name='roles'),
    url(r'^rol/crear/$', 'PIC.views.crearRol', name='crear_rol'), # ADD NEW PATTERN!
    url(r'^rol/modificar/(?P<id_rol>\d+)/$', 'PIC.views.modificar_rol'),
    url(r'^rol/consultar/(?P<id_rol>\d+)/$', 'PIC.views.consultar_roles'),
    url(r'^rol/eliminar/(?P<id_rol>.*)/$', 'PIC.views.eliminar_rol'),



#FLUJOS
    url(r'^flujo/nuevo/(?P<id_proyecto>\d+)/$','Flujo.views.nuevo_flujo'),
    url(r'^flujo/miflujo/(?P<id_proyecto>\d+)/$','Flujo.views.mi_flujo'),

#ACTIVIDADES
    url(r'^actividad/nueva/(?P<id_flujo>\d+)/$','Actividades.views.nueva_actividad'),
    url(r'^actividad/miactividad/(?P<id_actividad>\d+)/$','Actividades.views.mi_actividad'),
    url(r'^actividad/misactividades/(?P<id_proyecto>\d+)/$','Actividades.views.mis_actividades'),
)

