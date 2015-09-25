from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.views.generic.base import RedirectView
urlpatterns = patterns('',

    url(r'^files/', include('db_file_storage.urls')),
    url(r'^', include(admin.site.urls)),
    url(r'^reset/password_reset/$', 'django.contrib.auth.views.password_reset', name='admin_password_reset'),
    url(r'^reset/password_reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', name='password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),
    url(r'^accounts/login/', include(admin.site.urls) ),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),


#USUARIOS



    url(r'^usuario/lista/asignar/rol/(?P<id_rol>\d+)/$','PIC.views.lista_usuario_para_rol'),
    url(r'^usuario/asignar/rol/(?P<id_rol>\d+)//(?P<id_user>\d+)$','PIC.views.asignar_rol_usuario'),
    url(r'^usuario/nuevo/$', 'PIC.views.nuevo_usuario'),
    url(r'^usuarios/$','PIC.views.usuarios'),
    url(r'^usuario/eliminar/(?P<id_user>\d+)/$','PIC.views.desactivar_usuario'),
    url(r'^usuario/activar/(?P<id_user>\d+)/$','PIC.views.activar_usuario'),
    url(r'^usuario/editar/(?P<id_user>\d+)/$','PIC.views.editar_usuario'),



#PROYECTO
     url(r'^proyecto/menu/$','AdminProyectos.views.menu_proyecto'),
     url(r'^proyecto/nuevo$','AdminProyectos.views.nuevo_proyecto'),
     url(r'^proyectos/(?P<id_user>\d+)/$', 'AdminProyectos.views.proyectos'),
     url(r'^proyecto/editar/(?P<id_proyecto>\d+)/$','AdminProyectos.views.editar_proyecto'),
     url(r'^proyecto/iniciar/$','AdminProyectos.views.iniciar_proyecto'),
     url(r'^proyecto/eliminar/(?P<id_proyecto>\d+)/$','AdminProyectos.views.eliminar_proyecto'),
     url(r'^proyecto/pre/eliminar/(?P<id_proyecto>\d+)/$','AdminProyectos.views.pre_eliminar_proyecto'),
     url(r'^proyecto/miproyecto/(?P<id_proyecto>\d+)/$','AdminProyectos.views.mi_proyecto'),
     url(r'^proyecto/usuarios/(?P<id_proyecto>\d+)/$','AdminProyectos.views.listar_usuario_proyecto'),
     url(r'^proyecto/nousuarios/(?P<id_proyecto>\d+)/$','AdminProyectos.views.listar_usuarios_para_asignar_proyecto'),
     url(r'^proyecto/usuarios/asignar/(?P<id_proyecto>\d+)/(?P<id_user>\d+)/(?P<id_rol>\d+)/$','AdminProyectos.views.asignar_usuario_proyecto'),
     url(r'^proyecto/usuarios/desasignar/(?P<id_proyecto>\d+)/(?P<id_user>\d+)/$','AdminProyectos.views.desasignar_usuario_proyecto'),
     url(r'^proyecto/sin/finalizar/(?P<id_proyecto>\d+)/$','AdminProyectos.views.finalizar_proyecto'),



#ROLES

    url(r'^rol/listar/$', 'PIC.views.roles', name='roles'),
    url(r'^rol/crear/$', 'PIC.views.crearRol', name='crear_rol'), # ADD NEW PATTERN!
    url(r'^rol/modificar/(?P<id_rol>\d+)/$', 'PIC.views.modificar_rol'),
    url(r'^rol/consultar/(?P<id_rol>\d+)/$', 'PIC.views.consultar_roles'),
    url(r'^rol/eliminar/(?P<id_rol>.*)/$', 'PIC.views.eliminar_rol'),
    url(r'^proyecto/rol/(?P<id_proyecto>.*)/(?P<id_user>.*)/$', 'PIC.views.asignar_rol_a_user_proyecto'),



#FLUJOS
    url(r'^flujo/nuevo/(?P<id_proyecto>\d+)/$','Flujo.views.nuevo_flujo'),
    url(r'^flujo/miflujo/(?P<id_proyecto>\d+)/$','Flujo.views.mi_flujo'),


#ACTIVIDADES
    url(r'^actividad/nueva/(?P<id_proyecto>\d+)/$','Actividades.views.nueva_actividad'),
    url(r'^actividad/miactividad/(?P<id_actividad>\d+)/$','Actividades.views.mi_actividad'),
    url(r'^actividad/eliminar/(?P<id_proyecto>\d+)/(?P<id_actividad>\d+)/$','Actividades.views.eliminar_actividad'),
    url(r'^actividad/pre/eliminar/(?P<id_proyecto>\d+)/(?P<id_actividad>\d+)/$','Actividades.views.pre_eliminar_actividad'),
    url(r'^actividad/misactividades/(?P<id_proyecto>\d+)/$','Actividades.views.mis_actividades'),
    url(r'^actividad/misactividades/estados/(?P<id_proyecto>\d+)/(?P<id_actividad>\d+)/$','Actividades.views.ver_estados'),
    url(r'^actividad/editar/(?P<id_proyecto>\d+)/(?P<id_actividad>\d+)/$','Actividades.views.editar_actividad'),



 #SPRINT
     url(r'^sprint/nuevo/(?P<id_proyecto>\d+)/$','Sprint.views.nuevo_sprint'),
     url(r'^sprints/$', 'Sprint.views.sprints'),
     url(r'^sprint/editar/(?P<id_sprint>\d+)/$','Sprint.views.editar_sprint'),
     url(r'^sprint/iniciar/(?P<id_sprint>\d+)/$','Sprint.views.iniciar_sprint'),
     url(r'^sprint/eliminar/(?P<id_sprint>\d+)/$','Sprint.views.eliminar_sprint'),
    url(r'^sprint/pre/eliminar/(?P<id_sprint>\d+)/$','Sprint.views.pre_eliminar_sprint'),
     url(r'^sprint/missprints/(?P<id_proyecto>\d+)/$','Sprint.views.mis_sprints'),
     url(r'^sprint/misprint/(?P<id_sprint>\d+)/$','Sprint.views.mi_sprint'),
     url(r'^sprint/cerrar/(?P<id_sprint>\d+)/$','Sprint.views.cerrar_sprint'),
     url(r'^sprint/userstory/relacionados/(?P<id_sprint>\d+)/$','UserStory.views.lista_userstory_relacionado_a_sprint'),


#USERSTORY
     url(r'^userstory/nuevo/(?P<id_proyecto>\d+)/$','UserStory.views.nuevo_userstory'),
     url(r'^userstory/elimar/(?P<id_userstory>\d+)/$','UserStory.views.eliminar_userstory'),
     url(r'^userstory/pre/elimar/(?P<id_userstory>\d+)/$','UserStory.views.pre_eliminar_userstory'),
     url(r'^userstory/editar/(?P<id_userstory>\d+)/$','UserStory.views.editar_userstory'),
     url(r'^userstory/misuserstorys/(?P<id_proyecto>\d+)/$','UserStory.views.mis_userstorys'),
     url(r'^userstory/miuserstory/(?P<id_userstory>\d+)/$','UserStory.views.mi_userstory'),
     url(r'^userstory/miuserstory_reasignarActividad/(?P<id_proyecto>\d+)/(?P<id_actividad>\d+)/$','UserStory.views.lista_userstory_reasignarActividad',name='mi_userstory_reasignado'),
     url(r'^userstory/miuserstory/actividad/(?P<id_proyecto>\d+)/(?P<id_actividad>\d+)/(?P<id_userstory>\d+)/$','UserStory.views.asignar_userstory_a_actividad'),
     url(r'^userstory/miuserstory_no_creado/(?P<id_proyecto>\d+)/(?P<id_sprint>\d+)/$','UserStory.views.lista_userstory_no_creado'),
     url(r'^userstory/miuserstory/sprint/(?P<id_proyecto>\d+)/(?P<id_sprint>\d+)/(?P<id_userstory>\d+)/$','UserStory.views.asignar_userstory_a_sprint'),
     url(r'^usuario/userstory/lista/(?P<id_proyecto>\d+)/(?P<id_user>\d+)/$','UserStory.views.lista_userstory_creado_para_asignar_usuario'),
     url(r'^usuario/userstory/asignar/(?P<id_userstory>\d+)/(?P<id_user>\d+)/$','UserStory.views.asignar_usuario_userstory'),
     url(r'^userstory/actualizado/(?P<id_proyecto>\d+)/$','UserStory.views.cambiar_estado_todo'),
     url(r'^userstory/reasignar/(?P<id_proyecto>\d+)/(?P<id_sprint>\d+)/(?P<id_userstory>\d+)/$','UserStory.views.reasignar_userstory'),
     url(r'^userstory/desasignar/sprint/(?P<id_userstory>\d+)/(?P<id_sprint>\d+)/$','UserStory.views.desasinar_userstory_a_sprint'),

#COMENTARIOS

     url(r'^comentario/nuevo/(?P<id_userstory>\d+)/$','Comentario.views.nuevo_comentario'),
     url(r'^comentario/micomentario/(?P<id_comentario>\d+)/$','Comentario.views.mi_comentario'),
     url(r'^comentario/miscomentarios/(?P<id_userstory>\d+)/$','Comentario.views.mis_comentarios'),
     url(r'^comentario/adjunto/(?P<id_comentario>\d+)/$','Comentario.views.list'),
     url(r'^comentario/ver/adjunto/(?P<id_comentario>\d+)/$','Comentario.views.ver_archivo'),

#PROYECTO DESARRROLLO
     url(r'^proyecto/kanban/(?P<id_proyecto>\d+)/$','ProyectoDesarrollo.views.kanban'),
     url(r'^proyecto/sprint/visualizar/(?P<id_proyecto>\d+)/$','ProyectoDesarrollo.views.visualizar_sprint_en_desarrollo'),
     url(r'^proyecto/sprint/analizar/(?P<id_proyecto>\d+)/$','ProyectoDesarrollo.views.analizar_sprint'),
     url(r'^userstory/lista/actividad/reasignar/(?P<id_proyecto>\d+)/$','ProyectoDesarrollo.views.lista_reasignar_userstory_a_actividad'),
     url(r'^userstory/actividad/reasignar/(?P<id_proyecto>\d+)/(?P<id_userstory>\d+)/$','ProyectoDesarrollo.views.reasignar_userstory_a_actividad'),
     url(r'^userstory/lista/sprint/reasignar/(?P<id_proyecto>\d+)/$','ProyectoDesarrollo.views.lista_reasignar_userstory_a_sprint'),
     url(r'^userstory/sprint/reasignar/(?P<id_proyecto>\d+)/(?P<id_userstory>\d+)/$','ProyectoDesarrollo.views.reasignar_userstory_a_sprint'),

     #url(r'^proyecto/scrum_master/administracion/(?P<id_proyecto>\d+)/$','ProyectoDesarrollo.views.scrumMaster'),
     url(r'^proyecto/burndowncharts/(?P<id_proyecto>\d+)/$','ProyectoDesarrollo.views.Burndowncharts'),
     url(r'^proyecto/us/tiempo/nuevo/(?P<id_proyecto>\d+)/(?P<id_userstory>\d+)/$','ProyectoDesarrollo.views.reasignar_userstory_tiempo'),
     url(r'^proyecto/us/tiempo/(?P<id_proyecto>\d+)/$','ProyectoDesarrollo.views.lista_reasignar_userstory_tiempo'),
     url(r'^proyecto/aprobacion/us/finalizacion/(?P<id_proyecto>\d+)/$','ProyectoDesarrollo.views.lista_aprobacion_finalizacion'),


#ADMINISTRACION DEL SCRUM MASTER
    url(r'^proyecto/scrumMaster/(?P<id_proyecto>\d+)/$','AdminProyectos.views.scrum_master_vista'),
    url(r'^proyecto/scrumMaster/cliente/us/(?P<id_proyecto>\d+)/$','UserStory.views.listar_us_cliente'),
    url(r'^proyecto/scrumMaster/revision/us/(?P<id_proyecto>\d+)/$','UserStory.views.userstorys_revisar'),
    url(r'^userstory/cancelar/(?P<id_proyecto>\d+)/(?P<id_userstory>\d+)/$','UserStory.views.cancelar_userstory'),
    url(r'^userstory/lista/cancelar/(?P<id_proyecto>\d+)/$','UserStory.views.lista_userstory_cancelar'),
    url(r'^userstory/descancelar/(?P<id_proyecto>\d+)/(?P<id_userstory>\d+)/$','UserStory.views.descancelar_userstory'),
    url(r'^userstory/aprobar/finalizacion/(?P<id_userstory>\d+)/$','UserStory.views.aprobar_finalizacion'),

#CLIENTE
    url(r'^proyecto/cliente/menu/(?P<id_proyecto>\d+)/$','UserStory.views.menu_cliente'),
    url(r'^proyecto/cliente/nuevouserstory/(?P<id_proyecto>\d+)/$','UserStory.views.cliente_crear_userstory'),

#EQUIPO
    url(r'^proyecto/equipo/userstorys/(?P<id_proyecto>\d+)/$','UserStory.views.lista_userstory_usuario'),
    url(r'^proyecto/equipo/userstorys/finalizar/actividad/(?P<id_userstory>\d+)/$','UserStory.views.fin_de_una_actividad_de_un_us'),
    url(r'^proyecto/equipo/userstorys/iniciar/(?P<id_userstory>\d+)/$','UserStory.views.iniciar_userstory'),


##### graficas
    url(r'^BurnDownCharProyecto/(?P<id_proyecto>\d+)/$','AdminProyectos.views.jo3'),
    url(r'^BurnDownCharSprint/$','AdminProyectos.views.jo5'),
    url(r'^Sprint/BurnDownChar/(?P<id_proyecto>\d+)/$','AdminProyectos.views.lista_sprint_para_graficar'),
    url(r'^Sprint/BurnDownChar/ver/(?P<id_sprint>\d+)/$','AdminProyectos.views.jo5'),
#### pdfs

    url(r'^reporte01/(?P<id_proyecto>\d+)/$','AdminProyectos.views.reporte01'),
    url(r'^reporte02/(?P<id_proyecto>\d+)/$','AdminProyectos.views.reporte02'),
    url(r'^reporte03/(?P<id_proyecto>\d+)/$','AdminProyectos.views.reporte03'),
    url(r'^reporte04/(?P<id_proyecto>\d+)/$','AdminProyectos.views.reporte04'),
    url(r'^reporte05/(?P<id_proyecto>\d+)/$','AdminProyectos.views.reporte05'),
    url(r'^reporte06/(?P<id_proyecto>\d+)/$','AdminProyectos.views.reporte06'),
    url(r'^reportesPrincipal/(?P<id_proyecto>\d+)/$','AdminProyectos.views.lista_de_reportes'),


)
