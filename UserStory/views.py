# coding=UTF-8
from mx.DateTime.DateTime import today
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from UserStory.forms import UserStoryForm,UserStoryFormEdit
from UserStory.models import UserStory
from django.contrib import messages
from django.contrib.auth.decorators import login_required



def nuevo_userstory(request):
    """
    Crea un nuevo userstory
    """
    user=request.user
    #if not user.is_staff:
     #   return HttpResponseRedirect('/sinpermiso')
    if request.method=='POST':
        userstory_form = UserStoryForm(data=request.POST)


        # If the two forms are valid...
        if userstory_form.is_valid():
            # Guarda el Usuarios en la bd
            userstory_form.clean()
            nombre = userstory_form.cleaned_data['nombre']
            fecha_inicio = userstory_form.cleaned_data['fechaInicio']
            descripcion =  userstory_form.cleaned_data['descripcion']
            fechafin=userstory_form.cleaned_data['fechaFin']
            tiempo_trabajado=userstory_form.cleaned_data['tiempo_trabajado']
            porcentaje=userstory_form.cleaned_data['porcentaje']
            sprint=userstory_form.cleaned_data['sprint']
            estado=userstory_form.cleaned_data['estado']
            actividad=userstory_form.cleaned_data['actividad']




            userstory = UserStory()
            userstory.nombre=nombre
            userstory.fechaInicio=fecha_inicio
            userstory.fechaFin=fechafin
            userstory.fecha_creacion=today()
            userstory.estado=estado
            userstory.descripcion = descripcion
            userstory.tiempo_trabajado=tiempo_trabajado
            userstory.porcentaje=porcentaje
            userstory.sprint=sprint
            userstory.actividad=actividad
            userstory.save()
            messages.success(request, 'USER STORY CREADO CON EXITO!')
                        

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
            return HttpResponseRedirect('/userstory/miuserstory/'+str(userstory.id))
    else:
        userstory_form= UserStoryForm(request.POST)
    return render_to_response('HtmlUserStory/nuevouserstory.html',{'formulario':userstory_form,'user':user},
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

def iniciar_userstory(request, id_userstory):
    userstory= UserStory.objects.get(pk=id_userstory)
    userstory.estado='DOING'
    userstory.save()
    messages.success(request,'UserStory "'+userstory.nombre+'" doing')
    return HttpResponseRedirect('/userstory/miuserstory/'+str(id_userstory))

def editar_userstory(request, id_userstory):
 
    userstory= UserStory.objects.get(pk=id_userstory)
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
        formulario= UserStoryFormEdit(request.POST,instance=userstory)
        if formulario.is_valid():
            userstory= formulario.save()
            userstory.save()
            return HttpResponseRedirect('/userstory/miuserstory/'+str(id_userstory))
    else:
        formulario= UserStoryFormEdit(instance=userstory)
    return render_to_response('HtmlUserStory/editaruserstory.html',
                {'formulario':formulario,'id_userstory':id_userstory,'user':userstory.leader},
                              context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def userstorys(request):
    userstory = UserStory.objects.all()


    return render_to_response('HtmlUserStory/userstorys.html',
                {'userstory':userstory}, RequestContext(request))



def eliminar_userstory(request, id_userstory):
    userstory= UserStory.objects.get(pk=id_userstory)
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
    nombre=userstory.nombre
    userstory.delete()
    
    messages.success(request,"UserStory "+nombre+" Eliminado!")
    return HttpResponseRedirect('/userstorys/')

 
    return render_to_response('HtmlUserStory/eliminaruserstory.html',{'userstory':userstory},
                              context_instance=RequestContext(request))
def mis_userstorys(request):
    #query= "select p.nombre, p.id_proyecto from proyectos p right join rol_user r on r.proyecto_id = p.id_proyecto where r.user_id ="+str(request.user.id)
    userstorys_list=UserStory.objects.all()
    #proyectos_list=execute_query(query)
    
    #proyectos_list= Proyecto.objects.raw(query)
    return render_to_response('HtmlUserStory/misuserstorys.html',{'userstorys':userstorys_list})


def mi_userstory(request, id_userstory):
 
    userstory= UserStory.objects.get(pk=id_userstory)
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
        formulario= UserStoryFormEdit(request.POST,instance=userstory)
        if formulario.is_valid():
            userstory= formulario.save()
            userstory.save()
            return HttpResponseRedirect('/userstory/miuserstory/'+str(id_userstory))
    else:
        formulario= UserStoryFormEdit(instance=userstory)

    return render_to_response('HtmlUserStory/miuserstory.html',
                {'formulario':formulario,'userstory':userstory,
                 'id_userstory':id_userstory},
                              context_instance=RequestContext(request))


