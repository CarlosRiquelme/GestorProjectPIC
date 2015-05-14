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
     url(r'^proyecto/usuarios/(?P<id_proyecto>\d+)/$','AdminProyectos.views.listar_usuario_proyecto'),
     url(r'^proyecto/nousuarios/(?P<id_proyecto>\d+)/$','AdminProyectos.views.listar_usuarios_para_asignar_proyecto'),
     url(r'^proyecto/usuarios/asignar/(?P<id_proyecto>\d+)/(?P<id_user>\d+)/$','AdminProyectos.views.asignar_usuario_proyecto'),
    url(r'^proyecto/usuarios/desasignar/(?P<id_proyecto>\d+)/(?P<id_user>\d+)/$','AdminProyectos.views.desasignar_usuario_proyecto'),

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
    url(r'^actividad/misactividades/estados/(?P<id_proyecto>\d+)/(?P<id_actividad>\d+)/$','Actividades.views.ver_estados'),

 #SPRINT
     url(r'^sprint/nuevo/(?P<id_flujo>\d+)/$','Sprint.views.nuevo_sprint'),
     url(r'^sprints/$', 'Sprint.views.sprints'),
     url(r'^sprint/editar/(?P<id_sprint>\d+)/$','Sprint.views.editar_sprint'),
     url(r'^sprint/iniciar/(?P<id_sprint>\d+)/$','Sprint.views.iniciar_sprint'),
     url(r'^sprint/eliminar/(?P<id_sprint>\d+)/$','Sprint.views.eliminar_sprint'),
     url(r'^sprint/missprints/(?P<id_proyecto>\d+)/$','Sprint.views.mis_sprints'),
     url(r'^sprint/misprint/(?P<id_sprint>\d+)/$','Sprint.views.mi_sprint'),
     url(r'^sprint/cerrar/(?P<id_sprint>\d+)/$','Sprint.views.cerrar_sprint'),

#USERSTORY
     url(r'^userstory/nuevo/(?P<id_proyecto>\d+)/$','UserStory.views.nuevo_userstory'),
     #url(r'^userstorys/$', 'UserStory.views.userstorys'),
     #url(r'^userstory/editar/(?P<id_userstory>\d+)/$','UserStory.views.editar_userstory'),
     #url(r'^userstory/iniciar/(?P<id_userstory>\d+)/$','UserStory.views.iniciar_userstory'),
     #url(r'^userstory/eliminar/(?P<id_userstory>\d+)/$','UserStory.views.eliminar_userstory'),
     url(r'^userstory/misuserstorys/(?P<id_proyecto>\d+)/$','UserStory.views.mis_userstorys'),
     url(r'^userstory/miuserstory/(?P<id_userstory>\d+)/$','UserStory.views.mi_userstory'),
     url(r'^userstory/miuserstory_creado/(?P<id_proyecto>\d+)/(?P<id_actividad>\d+)/$','UserStory.views.lista_userstory_creado',name='mi_userstory_creado'),
     url(r'^userstory/miuserstory/actividad/(?P<id_proyecto>\d+)/(?P<id_actividad>\d+)/(?P<id_userstory>\d+)/$','UserStory.views.asignar_userstory_a_actividad'),
     url(r'^userstory/miuserstory_todo/(?P<id_proyecto>\d+)/(?P<id_actividad>\d+)/$','UserStory.views.lista_userstory_todo'),
     url(r'^userstory/miuserstory_doing/(?P<id_proyecto>\d+)/(?P<id_actividad>\d+)/$','UserStory.views.lista_userstory_doing'),
     url(r'^userstory/miuserstory_done/(?P<id_proyecto>\d+)/(?P<id_actividad>\d+)/$','UserStory.views.lista_userstory_done'),
     url(r'^userstory/miuserstory_no_creado/(?P<id_proyecto>\d+)/(?P<id_sprint>\d+)/$','UserStory.views.lista_userstory_no_creado'),
     url(r'^userstory/miuserstory/sprint/(?P<id_proyecto>\d+)/(?P<id_sprint>\d+)/(?P<id_userstory>\d+)/$','UserStory.views.asignar_userstory_a_sprint'),
     url(r'^usuario/userstory/lista/(?P<id_proyecto>\d+)/(?P<id_user>\d+)/$','UserStory.views.lista_userstory_creado_para_asignar_usuario'),
     url(r'^usuario/userstory/asignar/(?P<id_userstory>\d+)/(?P<id_user>\d+)/$','UserStory.views.asignar_usuario_userstory'),
#COMENTARIOS

     url(r'^comentario/nuevo/(?P<id_userstory>\d+)/$','Comentario.views.nuevo_comentario'),
     url(r'^comentario/micomentario/(?P<id_comentario>\d+)/$','Comentario.views.mi_comentario'),
     url(r'^comentario/miscomentarios/(?P<id_userstory>\d+)/$','Comentario.views.mis_comentarios'),
)

