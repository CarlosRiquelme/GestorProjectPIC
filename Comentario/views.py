# coding=UTF-8
from mx.DateTime.DateTime import today
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from Comentario.models import Comentario
from Comentario.forms import ComentarioForm
from django.contrib import messages
from UserStory.models import UserStory
from django.contrib.auth.decorators import login_required
from Flujo.models import Flujo


def nuevo_comentario(request, id_userstory):
    """
    Crea un nuevo comentario
    """
    user=request.user

    if request.method=='POST':
        comentario_form = ComentarioForm(data=request.POST)
        userstoty=UserStory.objects.get(pk=id_userstory)

        # If the two forms are valid...
        if comentario_form.is_valid():
            # Guarda el Usuarios en la bd
            comentario_form.clean()
            titulo= comentario_form.cleaned_data['titulo']
            descripcion =  comentario_form.cleaned_data['descripcion']
            adjunto = comentario_form.cleaned_data['adjunto']
            hora_trabajada=comentario_form.cleaned_data['hora_trabajada']
            porcentaje=comentario_form.cleaned_data['porcentaje']





            comentario = Comentario()
            suma=userstoty.tiempo_trabajado+comentario.hora_trabajada
            if suma <= userstoty.tiempo_estimado:
                comentario.titulo=titulo
                comentario.descripcion=descripcion
                comentario.adjunto=adjunto
                comentario.fecha_creacion=today()
                comentario.userstory_id=id_userstory
                comentario.porcentaje=porcentaje
                comentario.hora_trabajada=hora_trabajada
                comentario.save()
                userstoty.tiempo_trabajado=suma
                userstoty.porcentaje=porcentaje
                userstoty.save()
                messages.success(request, 'Comentario CREADO CON EXITO!')
                return HttpResponseRedirect('/comentario/micomentario/'+str(comentario.id))
            else:
                messages.success(request, 'Sobre paso la hora planificada FAVOR contacte con el SCRUM MASTER')
                return HttpResponseRedirect('proyectos/')

    else:
        comentario_form= ComentarioForm(request.POST)
    return render_to_response('HtmlComentario/nuevocomentario.html',{'formulario':comentario_form,'user':user,
                                                                     'id_userstory':id_userstory},
                              context_instance=RequestContext(request))


