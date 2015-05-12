# coding=UTF-8
from mx.DateTime.DateTime import today
from django.contrib.auth.models import User, Group, Permission
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from AdminProyectos.forms import ProyectoForm, ProyectoFormEdit
from AdminProyectos.models import Proyecto
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from Flujo.models import Flujo
from PIC.models import RolUsuarioProyecto


def nuevo_proyecto(request):
    """
    Crea un nuevo proyecto
    """
    user=request.user
    #if not user.is_staff:
     #   return HttpResponseRedirect('/sinpermiso')
    if request.method=='POST':
        proyecto_form = ProyectoForm(data=request.POST)


        # If the two forms are valid...
        if proyecto_form.is_valid():
            # Guarda el Usuarios en la bd
            proyecto_form.clean()
            nombre = proyecto_form.cleaned_data['nombre']
            fecha_inicio = proyecto_form.cleaned_data['fechaInicio']
            descripcion =  proyecto_form.cleaned_data['descripcion']
            scrumMaster = proyecto_form.cleaned_data['scrumMaster']
            fechafin=proyecto_form.cleaned_data['fechaFin']





            proyecto = Proyecto()
            proyecto.nombre=nombre
            proyecto.scrumMaster=scrumMaster
            proyecto.fechaInicio=fecha_inicio
            proyecto.fechaFin=fechafin
            proyecto.fecha_creacion=today()
            proyecto.estado='EN-ESPERA'
            proyecto.descripcion = descripcion
            proyecto.save()
            messages.success(request, 'PROYECTO CREADO CON EXITO!')
                        
            return HttpResponseRedirect('/proyecto/miproyecto/'+str(proyecto.id))
    else:
        proyecto_form= ProyectoForm(request.POST)
    return render_to_response('HtmlProyecto/nuevoproyecto.html',{'formulario':proyecto_form,'user':user},
                              context_instance=RequestContext(request))


def iniciar_proyecto(request, id_proyecto):
    proyecto= Proyecto.objects.get(pk=id_proyecto)
    proyecto.estado='INI'
    proyecto.save()
    messages.success(request,'Proyecto "'+proyecto.nombre+'" iniciado')
    return HttpResponseRedirect('/proyecto/miproyecto/'+str(id_proyecto))

def editar_proyecto(request, id_proyecto):
 
    proyecto= Proyecto.objects.get(pk=id_proyecto)
    user=request.user
    if request.method=='POST':
        formulario= ProyectoFormEdit(request.POST,instance=proyecto)
        if formulario.is_valid():
            proyecto= formulario.save()
            proyecto.save()
            return HttpResponseRedirect('/proyecto/miproyecto/'+str(id_proyecto))
    else:
        formulario= ProyectoFormEdit(instance=proyecto)
    return render_to_response('HtmlProyecto/editarproyecto.html',
                {'formulario':formulario,'id_proyecto':id_proyecto,'user':proyecto.scrumMaster},
                              context_instance=RequestContext(request))



def proyectos(request):
    proyecto = Proyecto.objects.all()


    return render_to_response('HtmlProyecto/proyectos.html',
                {'proyecto':proyecto}, RequestContext(request))



def eliminar_proyecto(request, id_proyecto):
    proyecto= Proyecto.objects.get(pk=id_proyecto)
    user=request.user
    nombre=proyecto.nombre
    proyecto.delete()
    
    messages.success(request,"Proyecto "+nombre+" Eliminado!")
    return HttpResponseRedirect('/proyectos/')

 
    return render_to_response('HtmlProyecto/eliminarproyecto.html',{'proyecto':proyecto},
                              context_instance=RequestContext(request))
def mis_proyectos(request):

    proyectos_list=Proyecto.objects.all()

    return render_to_response('HtmlProyecto/misproyectos.html',{'proyectos':proyectos_list})


def mi_proyecto(request, id_proyecto):
 
    proyecto= Proyecto.objects.get(pk=id_proyecto)
    if proyecto.estado == 'EN-DESARROLLO' :
        flujo=Flujo.objects.get(proyecto=id_proyecto)
    user=request.user
    if request.method=='POST':
        formulario= ProyectoFormEdit(request.POST,instance=proyecto)
        if formulario.is_valid():
            proyecto= formulario.save()
            proyecto.save()
            return HttpResponseRedirect('/proyecto/miproyecto/'+str(id_proyecto))
    else:
        formulario= ProyectoFormEdit(instance=proyecto)


    if proyecto.estado == 'EN-DESARROLLO' :
        return render_to_response('HtmlProyecto/miproyecto.html',
                                  {'formulario':formulario,'proyecto':proyecto,
                                   'id_proyecto':id_proyecto,'user':proyecto.scrumMaster,
                                   'flujo':flujo},context_instance=RequestContext(request))
    else:
        return render_to_response('HtmlProyecto/miproyecto.html',
                {'formulario':formulario,'proyecto':proyecto,
                 'id_proyecto':id_proyecto,'user':proyecto.scrumMaster},
                              context_instance=RequestContext(request))


def colaboradores(request, id_proyecto):
    #===========================================================================
    # rol_user=RolUser.objects.filter(proyecto_id=id_proyecto).exclude(user_id=request.user.id)
    # roles=RolUser.objects.all()
    #===========================================================================
    return render_to_response('HtmlProyecto/colaboradores.html',
                              {'roles_user':'',#rol_user,
                               'id_proyecto':id_proyecto, 'roles':'',#roles
                               })
def listar_usuario_proyecto(request, id_proyecto):
    usuarioproyecto=RolUsuarioProyecto.objects.filter(proyecto_id=id_proyecto)
    proyecto=Proyecto.objects.get(pk=id_proyecto)

    return render_to_response('HtmlProyecto/lista_usuario_proyecto.html',{'usuarioproyecto':usuarioproyecto,
                                                                          'id_proyecto':id_proyecto, 'proyecto':proyecto},
                              context_instance=RequestContext(request))
def asignar_usuario_proyecto(request, id_proyecto,id_user):

    usuarioproyecto=RolUsuarioProyecto()
    usuarioproyecto.proyecto_id=id_proyecto
    usuarioproyecto.usuario_id=id_user
    usuarioproyecto.save()
    messages.success(request, 'USUARIO ASIGNADO AL PROYECTO CORRECTAMENTE!')
    return HttpResponseRedirect('/proyecto/usuarios/'+str(id_proyecto))

def listar_usuarios_para_asignar_proyecto(request, id_proyecto):
    lista=[]
    usuarioproyecto=RolUsuarioProyecto.objects.filter(proyecto_id=id_proyecto)
    usuarios=User.objects.all()
    for user in usuarios:
        ban=1
        for user2 in usuarioproyecto:
            if user2.usuario.id == user.id: #si existe un usurio ya en tabla no quiero
                ban=0
        if ban == 1:
            lista.append(user)
    return render_to_response('HtmlProyecto/usuarios_asignar_proyecto.html',{'lista':lista,'usuarioproyecto':usuarioproyecto,
                                                                             'id_proyecto':id_proyecto},
                              context_instance=RequestContext(request))

def desasignar_usuario_proyecto(request, id_proyecto,id_user):

    usuarioproyecto=RolUsuarioProyecto.objects.get(usuario_id=id_user, proyecto_id=id_proyecto)
    usuarioproyecto.delete()
    messages.success(request, 'USUARIO DESASIGNADO AL PROYECTO CORRECTAMENTE!')
    return HttpResponseRedirect('/proyecto/usuarios/'+str(id_proyecto))

def listar_roles_para_asignar_usuario(request, id_proyecto):
    roles=Group.objects.all()
    usuarioproyecto=RolUsuarioProyecto.objects.filter(proyecto_id=id_proyecto)

    return render_to_response('HtmlProyecto/usuarios_asignar_proyecto.html',{'roles':roles,'usuarioproyecto':usuarioproyecto,
                                                                             'id_proyecto':id_proyecto},
                              context_instance=RequestContext(request))

