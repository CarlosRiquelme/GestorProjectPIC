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
from UserStory.models import UserStory
from django.contrib import messages
from django.contrib.auth.decorators import login_required



def nuevo_sprint(request):
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
            fechaInicio = sprint_form.cleaned_data['fechaInicio']
            fechaFin=sprint_form.cleaned_data['fechaFin']
            tiempo_acumulado =  sprint_form.cleaned_data['tiempo_acumulado']



            sprint = Sprint()


            for var in UserStory.objects.filter(sprint= sprint.id):
                suma = ++var.tiempo_trabajado

            sprint.nombre=nombre
            sprint.fechaInicio=fechaInicio
            sprint.fechaFin=fechaFin
            sprint.fecha_creacion=today()
            sprint.tiempo_acumulado=suma
            sprint.save()
            messages.success(request, 'SPRINT CREADO CON EXITO!')


            #aux = Rol.objects.filter(nombre='Leader').count()
            #===================================================================
            # if aux == 0:
            #    rol= crearRolLeader()
            # else:
            #     rol = Rol.objects.get(nombre='Leader')
            # rol_user=RolUser()
            # rol_user.rol = rol
            # rol_user.proyecto = proyecto
            # rol_user.user = user
            # rol_user.save()
            #===================================================================
            return HttpResponseRedirect('/sprint/misprint/'+str(sprint.id))
    else:
        sprint_form= SprintForm(request.POST)
    return render_to_response('HtmlSprint/nuevosprint.html',{'formulario':sprint_form,'user':user},
                              context_instance=RequestContext(request))

#===============================================================================
# def crearRolLeader():
#     permiso=Permisos()
#     permiso.AdminFase=True
#     permiso.AdminItem=True
#     permiso.AdminRol=True
#     permiso.AdminProyecto=True
#     permiso.AdminUser=True
#     permiso.save()
#     rol=Rol()
#     rol.nombre='Leader'
#     rol.permisos=permiso
#     rol.descripcion='Este rol tiene permiso absoluto sobre un proyecto'
#     rol.save()
#     return rol
#===============================================================================

def iniciar_sprint(request, id_sprint):
    sprint= Sprint.objects.get(pk=id_sprint)
    sprint.save()
    messages.success(request,'Proyecto "'+sprint.nombre+'" iniciado')
    return HttpResponseRedirect('/sprint/misprint/'+str(id_sprint))

def editar_sprint(request, id_sprint):

    sprint= Sprint.objects.get(pk=id_sprint)
    user=request.user
    #get_roles=RolUser.objects.filter(user=user,proyecto=proyecto)
 #==============================================================================
 #    if get_roles.count() == 0:
 #        return HttpResponseRedirect('/sinpermiso')
 #    for r in get_roles:
 #        if not r.rol.permisos.AdminProyecto:
 #            return HttpResponseRedirect('/sinpermiso')
 #
 #==============================================================================
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


@login_required(login_url='/ingresar')
def sprints(request):
    sprint = Sprint.objects.all()


    return render_to_response('HtmlSprint/sprints.html',
                {'sprint':sprint}, RequestContext(request))



def eliminar_sprint(request, id_sprint):
    sprint= Sprint.objects.get(pk=id_sprint)
    user=request.user
 #==============================================================================
 #    #get_roles=RolUser.objects.filter(user=user,proyecto=proyecto)
 #    if get_roles.count() == 0:
 #        return HttpResponseRedirect('/sinpermiso')
 #
 #    for r in get_roles:
 #        if not r.rol.permisos.delete_project:
 #            return HttpResponseRedirect('/sinpermiso')
 #
 #==============================================================================
    nombre=sprint.nombre
    sprint.delete()

    messages.success(request,"Sprint "+nombre+" Eliminado!")
    return HttpResponseRedirect('/sprints/')


    return render_to_response('HtmlSprint/eliminarsprint.html',{'sprint':sprint},
                              context_instance=RequestContext(request))
def mis_sprints(request):
    #query= "select p.nombre, p.id_proyecto from proyectos p right join rol_user r on r.proyecto_id = p.id_proyecto where r.user_id ="+str(request.user.id)
    sprints_list=Sprint.objects.all()
    #proyectos_list=execute_query(query)

    #proyectos_list= Proyecto.objects.raw(query)
    return render_to_response('HtmlSprint/missprints.html',{'sprints':sprints_list})


def mi_sprint(request, id_sprint):

    sprint= Sprint.objects.get(pk=id_sprint)
    user=request.user
    #get_roles=RolUser.objects.filter(user=user,proyecto=proyecto)
    #===========================================================================
    # if get_roles.count() == 0:
    #     return HttpResponseRedirect('/sinpermiso')
    # for r in get_roles:
    #     if not r.rol.permisos.AdminProyecto:
    #         return HttpResponseRedirect('/sinpermiso')
    #===========================================================================
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



