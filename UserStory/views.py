# coding=UTF-8
from mx.DateTime.DateTime import today
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from Actividades.models import Actividad
from UserStory.forms import UserStoryForm, UserStoryFormEdit, UserStoryClienteForm
from UserStory.models import UserStory, Historial_US, UserStory_aux
from django.contrib import messages
from Sprint.models import Sprint
from Comentario.models import Comentario
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from datetime import datetime, date, time, timedelta
from django.template.loader import render_to_string
from AdminProyectos.models import Proyecto
from PIC.models import RolUsuarioProyecto
from django.contrib.auth.models import User, Group, Permission
from django.core.exceptions import ObjectDoesNotExist
import smtplib





@login_required(login_url='/admin/login/')
def nuevo_userstory(request, id_proyecto):
    """
    Crea un nuevo userstory
    """
    user=request.user
    if request.method=='POST':
        userstory_form = UserStoryForm(data=request.POST)


        # If the two forms are valid...
        if userstory_form.is_valid():
            # Guarda el Usuarios en la bd
            userstory_form.clean()
            nombre = userstory_form.cleaned_data['nombre']
            descripcion =  userstory_form.cleaned_data['descripcion']
            prioridad=userstory_form.cleaned_data['prioridad']
            tiempo_estimado=userstory_form.cleaned_data['tiempo_estimado']
            userstory = UserStory()
            userstory.nombre=nombre
            userstory.descripcion = descripcion
            userstory.fecha_creacion=today()
            userstory.estado='CREADO'
            userstory.prioridad=prioridad
            userstory.tiempo_trabajado=0
            userstory.porcentaje=0
            userstory.proyecto_id=id_proyecto
            userstory.tiempo_estimado=tiempo_estimado
            # user_story2=UserStory_aux()
            # user_story2.nombre=nombre
            # user_story2.descripcion = descripcion
            # user_story2.fecha_creacion=today()
            # user_story2.estado='CREADO'
            # user_story2.prioridad=prioridad
            # user_story2.tiempo_trabajado=0
            # user_story2.porcentaje=0
            # user_story2.proyecto_id=id_proyecto
            # user_story2.tiempo_estimado=tiempo_estimado
            userstory.save()
            #user_story2.save()
            historial = Historial_US()
            historial.us_id=userstory.id
            historial.nombre_us=nombre
            historial.proyecto_id=id_proyecto
            historial.fecha=today()
            historial.descripcion="Creado por "+user.username
            historial.save()
            messages.success(request, 'USER STORY CREADO CON EXITO!')

            return HttpResponseRedirect('/userstory/misuserstorys/'+str(id_proyecto))
    else:
        userstory_form= UserStoryForm(request.POST)
    return render_to_response('HtmlUserStory/nuevouserstory.html',{'formulario':userstory_form,'user':user,
                                                                   'id_proyecto':id_proyecto},
                              context_instance=RequestContext(request))

@login_required(login_url='/admin/login/')
def iniciar_userstory(request, id_userstory):
    user=request.user
    userstory= UserStory.objects.get(pk=id_userstory)
    id_proyecto=userstory.proyecto.id
    historial_us=Historial_US()
    historial_us.us_id=userstory.id
    historial_us.nombre_us=userstory.nombre
    historial_us.fecha=today()
    historial_us.proyecto=userstory.proyecto_id
    historial_us.descripcion="Fue Iniciado por "+user.username+", paso al Estado DOING"
    userstory.estado='DOING'
    userstory.save()
    historial_us.save()
    messages.success(request,'UserStory "'+userstory.nombre+'" doing')
    return HttpResponseRedirect('/userstory/misuserstorys/'+str(id_proyecto))
@login_required(login_url='/admin/login/')
def editar_userstory(request, id_userstory):
    """
    Funcion donde el scrum master modifica el user story creado por el cliente
    :param request:
    :param id_userstory:
    :return:
    """
    user=request.user
    userstory= UserStory.objects.get(pk=id_userstory)
    id_proyecto=userstory.proyecto.id
    if userstory.sprint is None:
        if request.method=='POST':
            formulario= UserStoryFormEdit(request.POST,instance=userstory)
            if formulario.is_valid():
                userstory= formulario.save()
                historial_us=Historial_US()
                historial_us.us_id=userstory.id
                historial_us.nombre_us=userstory.nombre
                historial_us.fecha=today()
                historial_us.proyecto_id=userstory.proyecto_id
                historial_us.descripcion="Fue Editado por "+user.username
                userstory.save()
                historial_us.save()
                completar_atributos_userstory(id_userstory)
                return HttpResponseRedirect('/userstory/misuserstorys/'+str(id_proyecto))
        else:
            formulario= UserStoryFormEdit(instance=userstory)

        return render_to_response('HtmlUserStory/editaruserstory.html',
                    {'formulario':formulario,'id_userstory':id_userstory},
                                  context_instance=RequestContext(request))
    else:
        messages.success(request,"No se puede editar el US por estar relacionado a un Sprint")
        return HttpResponseRedirect('/userstory/misuserstorys/'+str(id_proyecto))

@login_required(login_url='/admin/login/')
def eliminar_userstory(request, id_userstory):
    user=request.user
    userstory= UserStory.objects.get(pk=id_userstory)
    historial_us=Historial_US()
    historial_us.nombre_us=userstory.nombre
    historial_us.fecha=today()
    historial_us.proyecto_id=userstory.proyecto_id
    historial_us.descripcion="Fue Eliminado por "+user.username
    historial_us.save()
    id_proyecto=userstory.proyecto_id
    user=request.user
    nombre=userstory.nombre
    userstory.delete()
    messages.success(request,"User Story "+nombre+" Eliminado!")
    return HttpResponseRedirect('/userstory/misuserstorys/'+str(id_proyecto))

def pre_eliminar_userstory(request, id_userstory):
    user=request.user
    userstory=UserStory.objects.get(pk=id_userstory)
    id_proyecto=userstory.proyecto_id
    print id_proyecto
    return render_to_response('HtmlUserStory/eliminaruserstory.html',{'userstory':userstory,
                                                                    'user':user,
                                                                    'id_proyecto':id_proyecto},
                             context_instance=RequestContext(request))

def completar_atributos_userstory(id_userstory):
    """
    Funcion donde se completa los atributo que faltan modificar en un user story
    una ves que el scrum Master modifica el user story del cliente
    :param id_userstory:
    :return:
    """
    userstory=UserStory.objects.get(pk=id_userstory)
    userstory.estado='CREADO'
    userstory.save()



@login_required(login_url='/admin/login/')
def mis_userstorys(request, id_proyecto):
    userstorys=UserStory.objects.filter(proyecto_id=id_proyecto).order_by('prioridad')
    proyecto=Proyecto.objects.get(pk=id_proyecto)
    rol=Group.objects.get(name='ScrumMaster')
    user=request.user
    rol_proyecto=RolUsuarioProyecto.objects.get(proyecto_id=id_proyecto, usuario_id=user.id)
    permiso=False
    print rol_proyecto.rol
    if rol_proyecto.rol == rol:
        permiso=True
    paginator=Paginator(userstorys,10)
    page=request.GET.get('page')
    try:
        userstorys=paginator.page(page)
    except PageNotAnInteger:
        userstorys=paginator.page(1)
    except EmptyPage:
        userstorys=paginator.page(paginator.num_pages)
    return render_to_response('HtmlUserStory/misuserstorys.html',{'userstorys':userstorys,
                                                                  'proyecto':proyecto,
                                                                  'user':user,
                                                                  'permiso':permiso})

@login_required(login_url='/admin/login/')
def mi_userstory(request, id_userstory):

    userstory= UserStory.objects.get(pk=id_userstory)
    user=request.user

    return render_to_response('HtmlUserStory/miuserstory.html',
                { 'userstory':userstory }, RequestContext(request))

@login_required(login_url='/admin/login/')
def asignar_userstory_a_actividad(request,id_proyecto ,id_actividad, id_userstory ):
    userstory=UserStory.objects.get(pk=id_userstory)
    actividad=Actividad.objects.get(pk=id_actividad)
    user=request.user
    userstory.actividad_id=id_actividad
    historial_us=Historial_US()
    historial_us.nombre_us=userstory.nombre
    historial_us.us_id=userstory.id
    historial_us.fecha=today()
    historial_us.descripcion="Fue asignado a la Actividad "+actividad.nombre+" por el usuario "+user.username
    historial_us.proyecto_id=id_proyecto
    userstory.save()
    historial_us.save()
    messages.success(request, 'USER STORY ASIGNADO A UNA ACTIVIDAD CORRECTAMENTE!')
    return HttpResponseRedirect('/userstory/misuserstorys/'+str(id_proyecto))

@login_required(login_url='/admin/login/')
def lista_userstory_reasignarActividad(request,id_proyecto, id_actividad):
     userstorys=UserStory.objects.filter(proyecto_id=id_proyecto)
     actividad=Actividad.objects.get(pk=id_actividad)

     return render_to_response('HtmlUserStory/userstory_reasignarActividad.html',{'userstorys':userstorys,'id_proyecto':id_proyecto,
                                                                       'id_actividad':id_actividad,'actividad':actividad})
@login_required(login_url='/admin/login/')
def lista_userstory_no_creado(request,id_proyecto, id_sprint):
     userstorys=UserStory.objects.filter(proyecto_id=id_proyecto)
     sprint=Sprint.objects.get(pk=id_sprint)

     return render_to_response('HtmlUserStory/userstory_no_creado.html',{'userstorys':userstorys,'id_proyecto':id_proyecto,
                                                                       'id_sprint':id_sprint,'sprint':sprint})
@login_required(login_url='/admin/login/')
def asignar_userstory_a_sprint(request,id_proyecto ,id_sprint, id_userstory ):
    user=request.user
    userstory=UserStory.objects.get(pk=id_userstory)
    sprint=Sprint.objects.get(pk=id_sprint)
    valor=sprint.tiempo_acumulado
    if (valor < userstory.tiempo_estimado):
        sprint.tiempo_acumulado=userstory.tiempo_estimado
    userstory.sprint_id=id_sprint
    sprint.suma_tiempo_usestory+=userstory.tiempo_trabajado
    historial_us=Historial_US()
    historial_us.nombre_us=userstory.nombre
    historial_us.us_id=userstory.id
    historial_us.fecha=today()
    historial_us.descripcion="Fue asignado al Sprint "+sprint.nombre+" por el usuario "+user.username
    historial_us.proyecto_id=id_proyecto
    historial_us.save()
    sprint.save()
    userstory.save()
    messages.success(request, 'USER STORY ASIGNADO A UNA SPRINT CORRECTAMENTE!')
    return HttpResponseRedirect('/userstory/miuserstory_no_creado/'+str(id_proyecto)+'/'+str(id_sprint))
@login_required(login_url='/admin/login/')
def lista_userstory_relacionado_a_sprint(request,id_sprint):
    userstory=UserStory.objects.filter(sprint_id=id_sprint)
    sprint=Sprint.objects.get(pk=id_sprint)
    user=request.user
    permiso=RolUsuarioProyecto.objects.get(proyecto_id=sprint.proyecto_id, usuario_id=user.id)
    proyecto=Proyecto.objects.get(pk=sprint.proyecto_id)

    return render_to_response('HtmlSprint/lista_userstory_sprint.html',{'userstory':userstory,'sprint':sprint,
                                                                       'id_sprint':id_sprint,
                                                                       'user':user,
                                                                       'permiso':permiso,
                                                                       'proyecto':proyecto})
@login_required(login_url='/admin/login/')
def desasinar_userstory_a_sprint(request, id_userstory,id_sprint):
    user=request.user
    userstory=UserStory.objects.get(pk=id_userstory)
    userstory.sprint_id=''
    userstory.save()
    userstory2=UserStory.objects.filter(sprint_id=id_sprint)
    valor=0
    sprint=Sprint.objects.get(pk=id_sprint)
    for dato in userstory2:
        if dato.tiempo_estimado > valor:
            valor=dato.tiempo_estimado
    sprint.tiempo_acumulado=valor
    historial_us=Historial_US()
    historial_us.nombre_us=userstory.nombre
    historial_us.us_id=id_userstory
    historial_us.fecha=today()
    historial_us.descripcion="Fue desasignado del Sprint "+sprint.nombre+" por el usuario "+user.username
    historial_us.proyecto_id=sprint.proyecto_id
    historial_us.save()
    sprint.save()
    messages.success(request, 'USER STORY DESASIGNADO A UNA SPRINT CORRECTAMENTE!')
    return HttpResponseRedirect('/sprint/userstory/relacionados/'+str(id_sprint))
@login_required(login_url='/admin/login/')
def asignar_usuario_userstory(request, id_userstory, id_user):
    user=request.user
    userstory=UserStory.objects.get(pk=id_userstory)
    usuario=User.objects.get(pk=id_user)
    id_proyecto=userstory.proyecto_id
    userstory.usuario_id=id_user
    userstory.save()
    historial_us=Historial_US()
    historial_us.nombre_us=userstory.nombre
    historial_us.us_id=id_userstory
    historial_us.fecha=today()
    historial_us.descripcion="Fue Asignado al Usuario "+usuario.username+" por el usuario "+user.username
    historial_us.proyecto_id=id_proyecto
    historial_us.save()
    messages.success(request, 'USER STORY ASIGNADO USUARIO Al USERSTORY CORRECTAMENTE!')

    if(usuario.email != 'NULL'):
        email=usuario.email
        nombre=userstory.nombre
        proyectos=userstory.proyecto
        descripcion=userstory.descripcion
        proyecto=proyectos.nombre
        try:
            html_content = 'Fue asignado a un User Story "'+nombre+'" que trata sobre  '+descripcion+'  del proyecto '+proyecto
            send_mail('Asignacion User Story',html_content , 'gestorprojectpic@gmail.com',[email], fail_silently=False)
        except smtplib.socket.gaierror:
            return HttpResponseRedirect('/error/conexion/')

    else:
        messages.success(request, 'El Usuario No Posee email, para notificarle, pero igual fue asignado!')

    return HttpResponseRedirect('/proyecto/usuarios/'+str(id_proyecto))

@login_required(login_url='/admin/login/')
def lista_userstory_creado_para_asignar_usuario(request,id_proyecto, id_user):
     userstorys=UserStory.objects.filter(proyecto_id=id_proyecto)
     usuario=User.objects.get(pk=id_user)


     return render_to_response('HtmlUserStory/asignar_usuario_userstory.html',{'userstorys':userstorys,'id_proyecto':id_proyecto,
                                                                       'usuario':usuario})
@login_required(login_url='/admin/login/')
def cambiar_estado_todo(request, id_proyecto):
    lista=[]
    ahora = date.today()
    #fecha=today.strftime("%Y/%m/%d")
    userstory=UserStory.objects.filter(proyecto_id=id_proyecto)
    for objeto in userstory:
        if objeto.fechaInicio <= ahora and objeto.estado == 'CREADO':
            objeto.estado= 'TODO'
            objeto.save()
            lista.append(objeto)
    return render_to_response('HtmlUserStory/cambiar_estado_todo.html',{'lista':lista})

@login_required(login_url='/admin/login/')
def reasignar_userstory(request,id_proyecto,id_sprint,id_userstory):
    userstory=UserStory.objects.get(pk=id_userstory)
    userstorys=UserStory.objects.filter(sprint_id=id_sprint)
    comentarios=Comentario.objects.filter(userstory_id=id_userstory)
    sprint=Sprint.objects.get(pk=id_sprint)
    resta=0
    if userstory.tiempo_trabajado>userstory.tiempo_estimado:
        if userstory.porcentaje<100:
            resta=userstory.tiempo_trabajado-userstory.tiempo_estimado
    resta2=0
    total=0
    for us in userstorys:
        if us.porcentaje==100:
            if us.tiempo_trabajado<us.tiempo_estimado:
                resta2=us.tiempo_estimado-us.tiempo_trabajado
                total=total+resta2
    if resta<resta2:
        messages.success(request, 'Sobra tiempo en su sprint, puede continuar con su tarea')
    else:
        messages.success(request, 'No tiene mas tiempo el sprint, se reasignara, creando un nuevo sprint')
        return render_to_response('HtmlUserStory/reasignarUS.html',{'userstorys':userstory,'id_proyecto':id_proyecto,'id_sprint':id_sprint,'sprint':sprint})

@login_required(login_url='/admin/login/')
def cliente_crear_userstory(request, id_proyecto):
    """
    Vista para que el cliente cree user story y pase al scrumMaster que pula o modifique para
    su utilizacion en el proyecto

    :param request:
    :param id_proyecto:
    :return:
    """
    user=request.user
    if request.method=='POST':
        userstoryform = UserStoryClienteForm(data=request.POST)
        # If the two forms are valid...
        if userstoryform.is_valid():
            # Guarda el Usuarios en la bd
            userstoryform.clean()
            nombre = userstoryform.cleaned_data['nombre']
            descripcion =  userstoryform.cleaned_data['descripcion']
            prioridad=userstoryform.cleaned_data['prioridad']
            userstory = UserStory()
            userstory.nombre=nombre
            userstory.descripcion = descripcion
            userstory.fecha_creacion=today()
            userstory.estado='REVISAR'
            userstory.prioridad=prioridad
            userstory.tiempo_trabajado=0
            userstory.porcentaje=0
            userstory.proyecto_id=id_proyecto
            userstory.tiempo_estimado=0
            userstory.save()
            historial_us=Historial_US()
            historial_us.nombre_us=nombre
            historial_us.us_id=userstory.id
            historial_us.fecha=today()
            historial_us.descripcion="Fue creado por "+user.username
            historial_us.proyecto_id=id_proyecto
            historial_us.save()
            messages.success(request, 'USER STORY CREADO CON EXITO!')
            messages.success(request, 'SE HA ENVIADO AL SCRUM MASTER PARA SU REVISION!')
            return HttpResponseRedirect('/proyecto/cliente/menu/'+str(id_proyecto))

    else:
        userstoryform= UserStoryClienteForm(request.POST)
    return render_to_response('HtmlUserStory/nuevouserstoryCliente.html',{'formulario2':userstoryform,'user':user,
                                                                   'id_proyecto':id_proyecto},
                              context_instance=RequestContext(request))
@login_required(login_url='/admin/login/')
def menu_cliente(request, id_proyecto):
    """
    Menu principal del cliente donde se le da la opcion de crear User Story al proyecto
    :param request:
    :param id_proyecto:
    :return:
    """
    user=request.user
    proyecto=Proyecto.objects.get(pk=id_proyecto)
    return render_to_response('HtmlProyecto/cliente.html',{'user':user,
                                                                   'id_proyecto':id_proyecto,
                                                                   'proyecto':proyecto},
                              context_instance=RequestContext(request))
@login_required(login_url='/admin/login/')
def listar_us_cliente(request, id_proyecto):
    """
    Lista los User Story creado por el cliente para que vea el  Scrum Master en su Vista
    :param request:
    :param id_proyecto:
    :return:
    """
    userstorys=UserStory.objects.filter(proyecto_id=id_proyecto, estado='REVISAR')
    return render_to_response('HtmlUserStory/lista_userstory_cliente.html',{'userstorys':userstorys,
                                                                   'id_proyecto':id_proyecto},
                              context_instance=RequestContext(request))
@login_required(login_url='/admin/login/')
def lista_userstory_usuario(request, id_proyecto):
    """
    Lista  los User Story  que pertence al usuario del proyecto
    :param request:
    :param id_proyecto:
    :return:
    """
    proyecto=Proyecto.objects.get(pk=id_proyecto)
    user=request.user
    try:
        sprint=Sprint.objects.get(proyecto_id=id_proyecto, estado='ABIERTO')
    except ObjectDoesNotExist:
        sprint=""

    userstorys=UserStory.objects.filter(proyecto_id=id_proyecto,usuario_id=user.id).order_by('estado')
    return render_to_response('HtmlUserStory/lista_userstory_usuario.html',{'userstorys':userstorys,
                                                                   'id_proyecto':id_proyecto, 'user':user,
                                                                   'proyecto':proyecto,
                                                                   'sprint':sprint,
                                                                   },
                              context_instance=RequestContext(request))

def iniciar_userstory(request, id_userstory):
    userstory=UserStory.objects.get(pk=id_userstory)
    id_proyecto=userstory.proyecto.id
    userstory.estado='DOING'
    userstory.save()
    messages.success(request, 'SE HA INICIADO EL USER STORY')
    return HttpResponseRedirect('/proyecto/equipo/userstorys/'+str(id_proyecto))

@login_required(login_url='/admin/login/')
def userstorys_revisar(request, id_proyecto):
    """
    Una vista que lista acciones posibles para pueden reasignarce un user story a una activida, sprint o finalizarla
    :param request:
    :param id_proyecto:
    :return:
    """
    user=request.user
    return render_to_response('HtmlUserStory/userstory_revision.html',{'user':user,'id_proyecto':id_proyecto},
                              context_instance=RequestContext(request))
@login_required(login_url='/admin/login/')
def fin_de_una_actividad_de_un_us(request, id_userstory):
    """
    El User Story pasa al estado finalizado en una activida pero primero se le notifica al SM para
    su aprovacion
    :param request:
    :param id_userstory:
    :return:
    """
    user=request.user
    userstory=UserStory.objects.get(pk=id_userstory)
    id_proyecto=userstory.proyecto.id
    actividades=Actividad.objects.filter(proyecto_id=id_proyecto)
    actividad=userstory.actividad
    usuario=userstory.usuario.username
    proyecto=Proyecto.objects.get(pk=userstory.proyecto_id)
    email=proyecto.scrumMaster.email
    ultima_actividad=0
    for dato in actividades:
        if ultima_actividad < dato.secuencia:
            ultima_actividad=dato.secuencia
    if actividad.secuencia == ultima_actividad:
        userstory.estado='REVISAR_FIN'
        try:
            html_content = 'El Usuario "'+usuario+'" a finalizado la ultima Actividad de su User Story, Favor Aprobar User Story'
            send_mail('Finalizacion de la Ultima de las Actividad de un User Story',html_content , 'gestorprojectpic@gmail.com',[email], fail_silently=False)
        except smtplib.socket.gaierror:
            return HttpResponseRedirect('/error/conexion/')

        userstory.save()
        historial_us=Historial_US()
        historial_us.nombre_us=userstory.nombre
        historial_us.us_id=id_userstory
        historial_us.fecha=today()
        historial_us.descripcion="Finalizado todas sus Actividades, por el usuario "+user.username+" pasa a revision"
        historial_us.proyecto_id=id_proyecto
        historial_us.save()
        messages.success(request, 'A finalizado la Actividad, Espere la Aprobacion de ScrumMaster')
    else:
        userstory.estado='REVISAR_FIN_AC'
        try:
            html_content = 'El Usuario "'+usuario+'" a finalizado una Actividad de su User Story, Favor Aprobar User Story'
            send_mail('Finalizacion de la Actividad de un User Story',html_content , 'gestorprojectpic@gmail.com',[email], fail_silently=False)
        except smtplib.socket.gaierror:
            return HttpResponseRedirect('/error/conexion/')

        userstory.save()
        historial_us=Historial_US()
        historial_us.nombre_us=userstory.nombre
        historial_us.us_id=id_userstory
        historial_us.fecha=today()
        historial_us.descripcion="Finalizado la Actividad "+userstory.actividad.nombre+ ", por el usuario "+user.username+", pasa a revision"
        historial_us.proyecto_id=id_proyecto
        historial_us.save()
        messages.success(request, 'A finalizado la Actividad, Espere la Aprobacion de ScrumMaster')

    return HttpResponseRedirect('/userstory/miuserstory/'+str(id_userstory))
def lista_userstory_cancelar(request, id_proyecto):
    user=request.user
    userstorys=UserStory.objects.filter(proyecto_id=id_proyecto)
    return render_to_response('HtmlUserStory/lista_userstory_cancelar.html',{'user':user,'id_proyecto':id_proyecto,
                                                                       'userstorys':userstorys},
                              context_instance=RequestContext(request))

def cancelar_userstory(request,id_proyecto,id_userstory):
    user=request.user
    userstory=UserStory.objects.get(pk=id_userstory)
    userstory.estado='CANCELADO'
    userstory.save()
    historial_us=Historial_US()
    historial_us.nombre_us=userstory.nombre
    historial_us.us_id=id_userstory
    historial_us.fecha=today()
    historial_us.descripcion="Cancelado  , por el usuario "+user.username
    historial_us.proyecto_id=id_proyecto
    historial_us.save()
    messages.success(request, 'UserStory CANCELADO!!!')
    return HttpResponseRedirect('/userstory/lista/cancelar/'+str(id_proyecto))

def descancelar_userstory(request,id_proyecto,id_userstory):
    user=request.user
    userstory=UserStory.objects.get(pk=id_userstory)
    userstory.estado='CREADO'
    userstory.save()
    historial_us=Historial_US()
    historial_us.nombre_us=userstory.nombre
    historial_us.us_id=id_userstory
    historial_us.fecha=today()
    historial_us.descripcion="Descancelado  , por el usuario "+user.username
    historial_us.proyecto_id=id_proyecto
    historial_us.save()
    messages.success(request, 'UserStory DESCANCELADO!!!')
    return HttpResponseRedirect('/userstory/lista/cancelar/'+str(id_proyecto))

def aprobar_finalizacion(request,id_userstory):
    user=request.user
    userstory=UserStory.objects.get(pk=id_userstory)
    usuario=userstory.usuario.username
    email=userstory.usuario.email
    id_proyecto=userstory.proyecto.id
    proyecto=Proyecto.objects.get(pk=id_proyecto)
    userstory.estado='FINALIZADO'
    try:
        html_content = 'A sido aprobada la finalizacion de su User Story "'+userstory.nombre+'" del Proyecto '+proyecto.nombre+ ' por el Scrum Master ' +proyecto.scrumMaster.username
        send_mail('Aprobacion de Finalizacion de su User Story',html_content , 'gestorprojectpic@gmail.com',[email], fail_silently=False)
    except smtplib.socket.gaierror:
        return HttpResponseRedirect('/error/conexion/')
    try:
        html_content = 'Aprobo la finalizacion de su User Story "'+userstory.nombre+'" del Proyecto '+proyecto.nombre+ ' asignado al usuario ' +usuario
        send_mail('Aprobacion de Finalizacion de User Story',html_content , 'gestorprojectpic@gmail.com',[proyecto.scrumMaster.email], fail_silently=False)
    except smtplib.socket.gaierror:
        return HttpResponseRedirect('/error/conexion/')

    userstory.save()
    historial_us=Historial_US()
    historial_us.nombre_us=userstory.nombre
    historial_us.us_id=id_userstory
    historial_us.fecha=today()
    historial_us.descripcion="Aprobado de Finalizacion del User Story "+userstory.nombre+ "  , por el usuario "+user.username
    historial_us.proyecto_id=id_proyecto
    historial_us.save()
    messages.success(request, 'A aprobado correctamente el USER STORY')

    return HttpResponseRedirect('/proyecto/aprobacion/us/finalizacion/'+str(id_proyecto))
@login_required(login_url='/admin/login/')
def listar_historial_us(request, id_userstory):
    """
    Lista los usuarios de un proyecto
    :param request:
    :param id_proyecto:
    :return:
    """
    historial=Historial_US.objects.filter(us_id=id_userstory).order_by("fecha")
    userstory=UserStory.objects.get(pk=id_userstory)
    id_proyecto=userstory.proyecto.id
    paginator=Paginator(historial,10)
    page=request.GET.get('page')
    try:
        historial=paginator.page(page)
    except PageNotAnInteger:
        historial=paginator.page(1)
    except EmptyPage:
        historial=paginator.page(paginator.num_pages)

    return render_to_response('HtmlUserStory/lista_historial.html',{'historial':historial,
                                                                    'id_proyecto':id_proyecto,
                                                                    'userstory':userstory},
                              context_instance=RequestContext(request))
