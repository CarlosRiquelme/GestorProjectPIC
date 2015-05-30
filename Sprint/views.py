# coding=UTF-8
from django.shortcuts import render

from mx.DateTime.DateTime import today
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from Sprint.forms import SprintForm,SprintFormEdit
from Sprint.models import Sprint
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from UserStory.models import UserStory


def nuevo_sprint(request, id_proyecto):
    """
    Crea un nuevo sprint
    """
    user=request.user
    #if not user.is_staff:
     #   return HttpResponseRedirect('/sinpermiso')
    if request.method=='POST':
        sprint_form = SprintForm(data=request.POST)


        # If the two forms are valid...
        if sprint_form.is_valid():
            # Guarda el Usuarios en la bd
            sprint_form.clean()
            nombre = sprint_form.cleaned_data['nombre']
            secuencia=sprint_form.cleaned_data['secuencia']


            sprint = Sprint()
            sprint.nombre=nombre
            sprint.secuencia=secuencia
            sprint.fecha_creacion=today()
            sprint.tiempo_acumulado = 0
            sprint.proyecto_id=id_proyecto
            sprint.estado='EN-ESPERA'
            sprint.save()
            messages.success(request, 'SPRINT CREADO CON EXITO!')

            return HttpResponseRedirect('/sprint/misprint/'+str(sprint.id))
    else:
        sprint_form= SprintForm(request.POST)
    return render_to_response('HtmlSprint/nuevosprint.html',{'formulario':sprint_form,'user':user,'id_proyecto':id_proyecto},
                              context_instance=RequestContext(request))


def iniciar_sprint(request, id_sprint):
    sprint= Sprint.objects.get(pk=id_sprint)
    sprint.save()
    messages.success(request,'Proyecto "'+sprint.nombre+'" iniciado')
    return HttpResponseRedirect('/sprint/misprint/'+str(id_sprint))

def editar_sprint(request, id_sprint):

    sprint= Sprint.objects.get(pk=id_sprint)
    user=request.user
    #get_roles=RolUser.objects.filter(user=user,proyecto=proyecto)

    if request.method=='POST':
        formulario= SprintFormEdit(request.POST,instance=sprint)
        if formulario.is_valid():
            sprint= formulario.save()
            sprint.save()
            return HttpResponseRedirect('/sprint/misprint/'+str(id_sprint))
    else:
        formulario= SprintFormEdit(instance=sprint)
    return render_to_response('HtmlSprint/editarsprint.html',
                {'formulario':formulario,'id_sprint':id_sprint},
                              context_instance=RequestContext(request))



def sprints(request):
    sprint = Sprint.objects.all()


    return render_to_response('HtmlSprint/sprints.html',
                {'sprint':sprint}, RequestContext(request))



def eliminar_sprint(request, id_sprint):
    sprint= Sprint.objects.get(pk=id_sprint)
    user=request.user

    nombre=sprint.nombre
    sprint.delete()

    messages.success(request,"Sprint "+nombre+" Eliminado!")
    return HttpResponseRedirect('/sprints/')


    return render_to_response('HtmlSprint/eliminarsprint.html',{'sprint':sprint},
                              context_instance=RequestContext(request))
def mis_sprints(request,id_proyecto):

    sprints=Sprint.objects.filter(proyecto_id=id_proyecto)




    return render_to_response('HtmlSprint/missprints.html',{'sprints':sprints,'id_proyecto':id_proyecto})


def mi_sprint(request, id_sprint):

    sprint= Sprint.objects.get(pk=id_sprint)
    user=request.user
    if request.method=='POST':
        formulario= SprintFormEdit(request.POST,instance=sprint)
        if formulario.is_valid():
            sprint= formulario.save()
            sprint.save()
            return HttpResponseRedirect('/sprint/misprint/'+str(id_sprint))
    else:
        formulario= SprintFormEdit(instance=sprint)

    return render_to_response('HtmlSprint/misprint.html',
                {'formulario':formulario,'sprint':sprint,
                 'id_proyecto':id_sprint},
                              context_instance=RequestContext(request))

def cerrar_sprint(request, id_sprint):
    userstory=UserStory.objects.filter(sprint_id=id_sprint)
    sprint=Sprint.objects.get(pk=id_sprint)
    suma=0
    for us in userstory:
        suma=suma+us.tiempo_estimado
    sprint.tiempo_acumulado=suma
    sprint.estado='CERRADO'
    sprint.save()
    messages.success(request, 'SPRINT CERRADO CON EXITO!')
    return HttpResponseRedirect('/sprint/misprint/'+str(sprint.id))



