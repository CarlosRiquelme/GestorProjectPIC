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
from UserStory.models import UserStory
from django.contrib.auth.decorators import login_required
from AdminProyectos.models import Proyecto
from django.core.urlresolvers import reverse
from django.core.mail import send_mail

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

        # If the two forms are valid...
        if comentario_form.is_valid():
            # Guarda el Usuarios en la bd
            comentario_form.clean()
            titulo= comentario_form.cleaned_data['titulo']
            descripcion =  comentario_form.cleaned_data['descripcion']
            porcentaje_actividad=comentario_form.cleaned_data['porcentaje_actividad']

            if porcentaje_actividad == 100:
                comentario = Comentario()
                comentario.titulo=titulo
                comentario.descripcion=descripcion
                comentario.fecha_creacion=today()
                comentario.userstory_id=id_userstory
                comentario.porcentaje_actividad=porcentaje_actividad
                comentario.save()

                html_content = 'El Usuario   "'+userstory.usuario.username+'"  agrego un nuevo comentario al userstory  "' +userstory.nombre+ '" donde da como Finalizada la Actividad"' \
                           +userstory.actividad.nombre
                send_mail('Nuevo Comentario',html_content , 'gestorprojectpic@gmail.com', [proyecto.scrumMaster.email], fail_silently=False)

                html_content = 'Agrego correctamente su comentario del "'+userstory.nombre+'" donde dio como Finalizada la actividad "' +userstory.actividad.nombre+ \
                               'Se le ha notificado al ScrumMaster espere que le reasigne a una nueva Actividad'
                send_mail('Nuevo Comentario',html_content , 'gestorprojectpic@gmail.com', [user.email], fail_silently=False)

                userstory.porcentaje+=userstory.porcentaje_actividad
                if userstory.porcentaje > 100.0:
                    userstory.porcentaje=100.0
                if userstory.porcentaje <= 100.0 and userstory.porcentaje >= 99.0:
                    userstory.estado='FINALIZADO'
                    html_content = 'El Usuario   "'+userstory.usuario.username+'"  a finalizado su userstory  "' +userstory.nombre
                    send_mail('Finalizacion de UserStory',html_content , 'gestorprojectpic@gmail.com', [proyecto.scrumMaster.email], fail_silently=False)

                    html_content = 'A Finalizado el "'+userstory.nombre+'" pasa a revision al ScrumMaster "'
                    send_mail('Nuevo Comentario',html_content , 'gestorprojectpic@gmail.com', [user.email], fail_silently=False)
                    userstory.save()
                else:
                    userstory.estado='DONE'
                    userstory.save()
                messages.success(request, 'Comentario CREADO CON EXITO!')
                return HttpResponseRedirect('/comentario/micomentario/'+str(comentario.id))
            else:
                comentario = Comentario()
                comentario.titulo=titulo
                comentario.descripcion=descripcion
                comentario.fecha_creacion=today()
                comentario.userstory_id=id_userstory
                comentario.porcentaje_actividad=porcentaje_actividad
                comentario.save()

                html_content = 'El Usuario   "'+userstory.usuario.username+'"  agrego un nuevo comentario al userstory  "' +userstory.nombre+ '" donde  aun no termina la Actividad"'

                send_mail('Nuevo Comentario',html_content , 'gestorprojectpic@gmail.com', [proyecto.scrumMaster.email], fail_silently=False)

                html_content = 'Agrego correctamente su comentario del "'+userstory.nombre+'" donde no a terminado aun la actividad "'

                send_mail('Nuevo Comentario',html_content , 'gestorprojectpic@gmail.com', [user.email], fail_silently=False)

                messages.success(request, 'Agrego Correctamente su Comentario')
                userstory.estado='DOING'
                userstory.save()
                return HttpResponseRedirect('/comentario/micomentario/'+str(comentario.id))

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
    documents.comentario=comentario
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES or None, instance=documents)
        if form.is_valid():
            comentario.adjunto='TRUE'
            form.save()
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


def mi_comentario(request, id_comentario):

    comentario= Comentario.objects.get(pk=id_comentario)
    user=request.user

    return render_to_response('HtmlComentario/micomentario.html',
                { 'comentario':comentario }, RequestContext(request))

def mis_comentarios(request, id_userstory):
    lista=[]
    comentarios=Comentario.objects.filter(userstory_id=id_userstory)
    userstory=UserStory.objects.get(pk=id_userstory)
    archivos=Document.objects.all()

    for dato in comentarios:
        for dato1 in archivos:
            if dato.id == dato1.comentario.id:
                lista.append(dato1)

    return render_to_response('HtmlComentario/miscomentarios.html',{'comentarios':comentarios,'id_userstory':id_userstory,
                                                                  'userstory':userstory,'lista':lista})

