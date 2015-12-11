# coding=UTF-8
from mx.DateTime.DateTime import today
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from Comentario.models import Comentario, Document
from Comentario.forms import ComentarioForm, DocumentForm
from django.contrib import messages
from UserStory.models import UserStory, US_Estado_ultimo, Historial_US,UserStory_Sprint
from django.contrib.auth.decorators import login_required
from AdminProyectos.models import Proyecto
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
import smtplib
from PIC.models import RolUsuarioProyecto
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, date, time, timedelta
from ProyectoDesarrollo.views import que_dia_es
def nuevo_comentario(request, id_userstory):
    """
    Crea un nuevo comentario
    """
    user=request.user

    if request.method=='POST':
        comentario_form = ComentarioForm(data=request.POST)
        userstory=UserStory.objects.get(pk=id_userstory)
        id_proyecto=userstory.proyecto_id
        id_sprint=userstory.sprint_id
        proyecto=Proyecto.objects.get(pk=id_proyecto)
        user=request.user
        suma=0
        resta=0

        # If the two forms are valid...
        if comentario_form.is_valid():
            # Guarda el Usuarios en la bd
            comentario_form.clean()
            titulo= comentario_form.cleaned_data['titulo']
            descripcion =  comentario_form.cleaned_data['descripcion']
            hora_trabajada=comentario_form.cleaned_data['hora_trabajada']
            suma=userstory.tiempo_trabajado+hora_trabajada
            hora_trabajada2=hora_trabajada
            ahora = date.today()
            if userstory.tiempo_estimado > suma:
                comentario = Comentario()
                comentario.titulo=titulo
                comentario.descripcion=descripcion
                comentario.fecha_creacion=today()
                comentario.userstory_id=id_userstory
                comentario.hora_trabajada=hora_trabajada

                try:
                    html_content = 'El Usuario   "'+userstory.usuario.username+'"  agrego un nuevo comentario al userstory  " ' +userstory.nombre+ '" donde a trabajado "' \
                           +str(hora_trabajada)+' " horas en total en este user story'
                    send_mail('Nuevo Comentario',html_content , 'gestorprojectpic@gmail.com', [proyecto.scrumMaster.email], fail_silently=False)
                except smtplib.socket.gaierror:
                    return HttpResponseRedirect('/error/conexion/')
                try:
                    html_content = 'Agrego correctamente su comentario del "'+userstory.nombre+'" donde a trabajado " ' +str(hora_trabajada)+ \
                               ' " Se le ha notificado al ScrumMaster de esta accion'
                    send_mail('Nuevo Comentario',html_content , 'gestorprojectpic@gmail.com', [user.email], fail_silently=False)
                except smtplib.socket.gaierror:
                    return HttpResponseRedirect('/error/conexion/')

                comentario.save()
                ######
                try:
                    us_sprint=UserStory_Sprint.objects.get(sprint_id=userstory.sprint_id, fecha=ahora)
                except ObjectDoesNotExist:
                    us_sprint=''
                if us_sprint == '':
                    us_sprint=UserStory_Sprint()
                    us_sprint2=UserStory_Sprint.objects.filter(sprint_id=userstory.sprint_id).order_by('fecha')
                    suma_tiempo_trabajado=0
                    suma_tiempo_estimado=0
                    for i in us_sprint2:
                        suma_tiempo_trabajado+=i.horas_trabajadas
                        suma_tiempo_estimado=i.horas_estimada
                    us_sprint.horas_trabajadas=suma_tiempo_trabajado+hora_trabajada
                    us_sprint.horas_estimada=suma_tiempo_estimado
                else:
                    us_sprint.horas_trabajadas+=hora_trabajada
                us_sprint.sprint_id=userstory.sprint.id
                us_sprint.proyecto_id=id_proyecto
                us_sprint.fecha=ahora
                us_sprint.save()
                ######
                userstory.tiempo_trabajado=suma
                userstory.suma_trabajadas+=hora_trabajada2
                userstory.save()
                historial_us=Historial_US()
                historial_us.nombre_us=userstory.nombre
                historial_us.us_id=id_userstory
                historial_us.fecha=today()
                historial_us.descripcion="Fue agregado un comentario "+titulo+" , por el usuario "+user.username
                historial_us.proyecto_id=id_proyecto
                historial_us.save()
                messages.success(request, 'Agrego Correctamente su Comentario')
                return HttpResponseRedirect('/comentario/miscomentarios/'+str(comentario.userstory.id))
            else:
                resta=suma-userstory.tiempo_estimado
                bandera=True
                if resta == 0:
                    comentario = Comentario()
                    comentario.titulo=titulo
                    comentario.descripcion=descripcion
                    comentario.fecha_creacion=today()
                    comentario.userstory_id=id_userstory
                    comentario.hora_trabajada=hora_trabajada2
                    try:
                        html_content = 'El Usuario   "'+userstory.usuario.username+'"  agrego un nuevo comentario al userstory  "' +userstory.nombre+ '" donde a trabajado"' \
                               +str(userstory.tiempo_trabajado)+' " horas en total en este user story donde a finalizado su tiempo estimado   " '
                        send_mail('Nuevo Comentario - Finalizo su Tiempo de User Story',html_content , 'gestorprojectpic@gmail.com', [proyecto.scrumMaster.email], fail_silently=False)
                    except smtplib.socket.gaierror:
                        return HttpResponseRedirect('/error/conexion/')
                    try:
                        html_content = 'Agrego correctamente su comentario del "'+userstory.nombre+'" donde a trabajado "' +str(userstory.tiempo_trabajado)+ \
                                   'Se le ha notificado al ScrumMaster que alcanzo el tiempo estimado de su User Story'
                        send_mail('Nuevo Comentario',html_content , 'gestorprojectpic@gmail.com', [user.email], fail_silently=False)
                    except smtplib.socket.gaierror:
                        return HttpResponseRedirect('/error/conexion/')
                    comentario.save()
                    ######
                    try:
                        us_sprint=UserStory_Sprint.objects.get(sprint_id=userstory.sprint_id, fecha=ahora)
                    except ObjectDoesNotExist:
                        us_sprint=''
                    if us_sprint == '':
                        us_sprint=UserStory_Sprint()
                        us_sprint2=UserStory_Sprint.objects.filter(sprint_id=userstory.sprint_id).order_by('fecha')
                        suma_tiempo_trabajado=0
                        suma_tiempo_estimado=0
                        for i in us_sprint2:
                            suma_tiempo_trabajado+=i.horas_trabajadas
                            suma_tiempo_estimado=i.horas_estimada
                        us_sprint.horas_trabajadas=suma_tiempo_trabajado+hora_trabajada
                        us_sprint.horas_estimada=suma_tiempo_estimado
                    else:
                        us_sprint.horas_trabajadas+=hora_trabajada
                    us_sprint.fecha=ahora
                    us_sprint.proyecto_id=id_proyecto
                    us_sprint.sprint_id=userstory.sprint.id
                    us_sprint.save()
                    ######
                    try:
                        us_ultimo_estado=US_Estado_ultimo.objects.get(us_id=id_userstory)
                    except ObjectDoesNotExist:
                        us_ultimo_estado = ''
                    if us_ultimo_estado == '':
                        us_ultimo_estado=US_Estado_ultimo()
                        us_ultimo_estado.us_id=id_userstory
                        us_ultimo_estado.estado=userstory.estado
                        us_ultimo_estado.estado_actual='REVISAR_TIEMPO'
                        us_ultimo_estado.save()
                    if us_ultimo_estado != '':
                        us_ultimo_estado.estado=userstory.estado
                        us_ultimo_estado.estado_actual='REVISAR_TIEMPO'
                        us_ultimo_estado.save()
                    userstory.tiempo_trabajado+=hora_trabajada2
                    userstory.estado='REVISAR_TIEMPO'
                    userstory.suma_trabajadas+=hora_trabajada2
                    userstory.save()
                    historial_us=Historial_US()
                    historial_us.nombre_us=userstory.nombre
                    historial_us.us_id=id_userstory
                    historial_us.fecha=today()
                    historial_us.descripcion="Fue agregado un comentario "+titulo+" , por el usuario "+user.username+ ", pasa a revision por terminar el tiempo"
                    historial_us.proyecto_id=id_proyecto
                    historial_us.save()
                    messages.success(request, 'Agrego Correctamente su Comentario')
                    messages.success(request, 'A alcanzado su tiempo estimado de su User Story')
                    messages.success(request, 'Se comunico al Scrum Master')
                    return HttpResponseRedirect('/comentario/micomentario/'+str(comentario.id))
                else:
                    resta=suma-userstory.tiempo_estimado
                    comentario = Comentario()
                    comentario.titulo=titulo
                    comentario.descripcion=descripcion
                    comentario.fecha_creacion=today()
                    comentario.userstory_id=id_userstory
                    comentario.hora_trabajada=hora_trabajada


                    try:
                        html_content = 'El Usuario   "'+userstory.usuario.username+'"  agrego un nuevo comentario al userstory  "' +userstory.nombre+ '" donde a trabajado"' \
                           +str(userstory.tiempo_trabajado)+' " horas en total en este user story donde a finalizado su tiempo estimado   " '
                        send_mail('Nuevo Comentario - Finalizo su Tiempo de User Story',html_content , 'gestorprojectpic@gmail.com', [proyecto.scrumMaster.email], fail_silently=False)
                    except smtplib.socket.gaierror:
                        return HttpResponseRedirect('/error/conexion/')
                    try:
                        html_content = 'Agrego correctamente su comentario del "'+userstory.nombre+'" donde a trabajado "' +str(userstory.tiempo_trabajado)+ \
                               'Se le ha notificado al ScrumMaster que alcanzo el tiempo estimado de su User Story'
                        send_mail('Nuevo Comentario',html_content , 'gestorprojectpic@gmail.com', [user.email], fail_silently=False)
                    except smtplib.socket.gaierror:
                        return HttpResponseRedirect('/error/conexion/')
                    comentario.save()
                    ######

                    try:
                        us_sprint=UserStory_Sprint.objects.get(sprint_id=userstory.sprint_id,fecha=ahora)
                    except ObjectDoesNotExist:
                        us_sprint=''
                    if us_sprint == '' :
                        us_sprint=UserStory_Sprint()
                        us_sprint2=UserStory_Sprint.objects.filter(sprint_id=userstory.sprint_id).order_by('fecha')
                        suma_tiempo_trabajado=0
                        suma_tiempo_estimado=0
                        for i in us_sprint2:
                            suma_tiempo_trabajado+=i.horas_trabajadas
                            suma_tiempo_estimado=i.horas_estimada
                        us_sprint.horas_trabajadas=suma_tiempo_trabajado+hora_trabajada
                        us_sprint.horas_estimada=suma_tiempo_estimado
                    else:
                        us_sprint.horas_trabajadas+=hora_trabajada
                    us_sprint.fecha=ahora
                    us_sprint.proyecto_id=id_proyecto
                    us_sprint.sprint_id=userstory.sprint.id
                    us_sprint.save()
                    ######
                    try:
                        us_ultimo_estado=US_Estado_ultimo.objects.get(us_id=id_userstory)
                    except ObjectDoesNotExist:
                        us_ultimo_estado=''
                    if us_ultimo_estado == '':
                        us_ultimo_estado=US_Estado_ultimo()
                        us_ultimo_estado.us_id=id_userstory
                        us_ultimo_estado.estado=userstory.estado
                        us_ultimo_estado.estado_actual='REVISAR_TIEMPO'
                        us_ultimo_estado.save()
                    if us_ultimo_estado != '':
                        us_ultimo_estado.estado=userstory.estado
                        us_ultimo_estado.estado_actual='REVISAR_TIEMPO'
                        us_ultimo_estado.save()
                    userstory.tiempo_trabajado=suma-resta########################################################
                    userstory.estado='REVISAR_TIEMPO'
                    userstory.suma_trabajadas=userstory.suma_trabajadas+hora_trabajada
                    userstory.tiempo_demas=resta
                    userstory.save()
                    historial_us=Historial_US()
                    historial_us.nombre_us=userstory.nombre
                    historial_us.us_id=id_userstory
                    historial_us.fecha=today()
                    historial_us.descripcion="Fue agregado un comentario "+titulo+" , por el usuario "+user.username+ ", pasa a revision por sobre pasar su tiempo"
                    historial_us.proyecto_id=id_proyecto
                    historial_us.save()
                    messages.success(request, 'Agrego Correctamente su Comentario')
                    messages.success(request, 'A alcanzado su tiempo estimado de su User Story')
                    messages.success(request, 'Se comunico al Scrum Master')
                    return HttpResponseRedirect('/comentario/miscomentarios/'+str(userstory.id))

    else:
        comentario_form= ComentarioForm(request.POST)
    return render_to_response('HtmlComentario/nuevocomentario.html',{'formulario':comentario_form,'user':user,
                                                                     'id_userstory':id_userstory},
                              context_instance=RequestContext(request))

def list(request, id_comentario):
    # Handle file upload
    documents=Document()
    comentario=Comentario.objects.get(pk=id_comentario)
    userstory=UserStory.objects.get(pk=comentario.userstory.id)
    documents.comentario_id=comentario.id
    if request.method == 'POST':

        form = DocumentForm(request.FILES)
        print form.is_valid()
        if form.is_valid():
            comentario.adjunto='TRUE'
            comentario.save()
            archivo=form.save()
            archivo.save()
            documents.save()
            messages.success(request, 'Se a adjuntado correctamente el archivo')
            # Redirect to the document list after POST
            return HttpResponseRedirect('/comentario/miscomentarios/'+str(userstory.id))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page

    # Render list page with the documents and the form
    return render_to_response(
        'HtmlComentario/adjunto.html',
        {'form': form},
        context_instance=RequestContext(request)
    )

def ver_archivo(request, id_comentario):
    comentario=Comentario.objects.get(pk=id_comentario)
    existe=Document.objects.filter(comentario_id=id_comentario).exists()
    if existe:
        document=Document.objects.get(comentario_id=id_comentario)

    return render_to_response(
        'HtmlComentario/ver_adjunto.html',
        {'document': document.docfile,
         'comentario':comentario},
        context_instance=RequestContext(request)
    )



def mi_comentario(request, id_comentario):

    comentario= Comentario.objects.get(pk=id_comentario)
    user=request.user

    return render_to_response('HtmlComentario/micomentario.html',
                { 'comentario':comentario }, RequestContext(request))

def mis_comentarios(request, id_userstory):
    lista=[]
    user=request.user
    comentarios=Comentario.objects.filter(userstory_id=id_userstory)
    userstory=UserStory.objects.get(pk=id_userstory)
    archivos=Document.objects.all()
    id_proyecto=userstory.proyecto_id
    proyecto=Proyecto.objects.get(pk=id_proyecto)
    permiso=RolUsuarioProyecto.objects.get(proyecto_id=id_proyecto, usuario_id=user.id)
    for dato in comentarios:
        for dato1 in archivos:
            if dato.id == dato1.comentario.id:
                lista.append(dato1)
    paginator=Paginator(comentarios,5)
    page=request.GET.get('page')
    try:
        comentarios=paginator.page(page)
    except PageNotAnInteger:
        comentarios=paginator.page(1)
    except EmptyPage:
        comentarios=paginator.page(paginator.num_pages)


    return render_to_response('HtmlComentario/miscomentarios.html',{'comentarios':comentarios,'id_userstory':id_userstory,
                                                                  'userstory':userstory,
                                                                  'lista':comentarios,
                                                                  'id_proyecto':id_proyecto,
                                                                  'user':user,
                                                                  'proyecto':proyecto,
                                                                  'permiso':permiso})

def error_conexion():
    return render_to_response('HtmlProyecto/errorconexion.html')