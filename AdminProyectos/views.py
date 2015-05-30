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
from mx.DateTime.DateTime import today
from datetime import datetime, date, time, timedelta
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from PIC.models import RolUsuarioProyecto
from Sprint.models import Sprint, Estimacion_Proyecto, Estimacion_Sprint
from UserStory.models import UserStory
from Actividades.models import Actividad

@login_required(login_url='/admin/login/')
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

            proyecto = Proyecto()
            proyecto.nombre=nombre
            proyecto.scrumMaster=scrumMaster
            proyecto.fechaInicio=fecha_inicio
            proyecto.fecha_creacion=today()
            proyecto.estado='EN-ESPERA'
            proyecto.descripcion = descripcion
            usuario=User.objects.get(pk=scrumMaster.id)
            if usuario.email != 'NULL' and usuario.email != '':
                fecha=fecha_inicio
                email=usuario.email

                print email
                html_content = 'Fue asignado a un Proyecto '+nombre+' ' \
                                                                    'Descripcion:'+descripcion+' ' \
                                                                                                   'Fecha Inicio:'+fecha.strftime('%Y/%m/%d')
                send_mail('Asignado a Proyecto',html_content , 'gestorprojectpic@gmail.com', [email], fail_silently=False)
            proyecto.save()
            rol=Group.objects.get(name='ScrumMaster')
            rolproyecto=RolUsuarioProyecto()
            rolproyecto.usuario_id=usuario.id
            rolproyecto.rol=rol
            rolproyecto.proyecto_id=proyecto.id
            rolproyecto.save()
            messages.success(request, 'PROYECTO CREADO CON EXITO!')
                        
            return HttpResponseRedirect('/proyecto/menu/')
    else:
        proyecto_form= ProyectoForm()
    return render_to_response('HtmlProyecto/nuevoproyecto.html',{'formulario':proyecto_form,'user':user},
                              context_instance=RequestContext(request))

@login_required(login_url='/admin/login/')
def iniciar_proyecto(request):
    lista=[]
    ahora = date.today()
    proyectos=Proyecto.objects.all()
    for objeto in proyectos:
        if objeto.fechaInicio <= ahora and objeto.estado == 'EN-ESPERA':
            scrum_master=objeto.scrumMaster
            fecha=objeto.fechaInicio
            html_content = 'Su Proyecto "'+objeto.nombre+'"  a iniciado por llegar su fecha de Inicio  '+fecha.strftime('%Y/%m/%d')
            send_mail('Asignado a Proyecto',html_content , 'gestorprojectpic@gmail.com', [scrum_master.email], fail_silently=False)

            objeto.estado= 'EN-DESARROLLO'
            sprint=Sprint.objects.filter(proyecto_id=objeto.id).order_by("secuencia")
            fecha1=fecha
            estimacion_proyecto=Estimacion_Proyecto()
            estimacion_proyecto.fechaInicio=objeto.fechaInicio
            estimacion_proyecto.proyecto_id=objeto.id
            estimacion_proyecto.save()
            userstorys=UserStory.objects.filter(proyecto_id=objeto.id)
            uno=1
            actividad=Actividad.objects.get(proyecto_id=objeto.id , secuencia=uno)
            actividades=Actividad.objects.filter(proyecto_id=objeto.id)
            cantidad_actividades=0
            peso_actividad=0.0
            for dato in actividades:
                cantidad_actividades+=1
            peso_actividad=100/cantidad_actividades
            for dato in userstorys:
                dato.actividad_id=actividad.id
                dato.porcentaje_actividad=peso_actividad
                dato.estado='TODO'
                dato.save()

            for dato in sprint:
                sprint1=Sprint.objects.get(pk=dato.id)
                estimacion_sprint=Estimacion_Sprint()
                estimacion_sprint.proyecto_estimacion_id=estimacion_proyecto.id
                estimacion_sprint.sprint_id=dato.id
                estimacion_sprint.fechaInicio=fecha1
                sprint1.fechaInicio=fecha1
                dias= dato.tiempo_acumulado/8
                fecha2=fecha_calcular(fecha1,dias)
                estimacion_sprint.fechaFin=fecha2
                fecha1=fecha_calcular(fecha2,1)
                sprint1.fechaFin=fecha2
                sprint1.dias_duracion=dias
                sprint1.dia_trancurrido=0
                estimacion_sprint.duracion=dato.tiempo_acumulado
                sprint1.save()
                estimacion_sprint.save()
            sprint2=Sprint.objects.get(proyecto_id=objeto.id, fechaInicio=fecha)
            sprint2.estado='ABIERTO'
            sprint2.save()
            estimacion_proyecto=Estimacion_Proyecto.objects.get(proyecto_id=objeto.id)
            estimacion_proyecto.fechaFin=fecha2
            objeto.fechaFin=fecha2
            estimacion_proyecto.save()
            objeto.save()
            lista.append(objeto)

    return render_to_response('HtmlProyecto/lista_proyectos_iniciados.html',{'lista':lista})

@login_required(login_url='/admin/login/')
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
@login_required(login_url='/admin/login/')
def menu_proyecto(request):
    user=request.user
    return render_to_response('HtmlProyecto/menu_proyecto.html',{'user':user})

@login_required(login_url='/admin/login/')
def proyectos(request,id_user):
    usuarioproyecto=RolUsuarioProyecto.objects.filter(usuario_id=id_user)
    user=request.user

    return render_to_response('HtmlProyecto/proyectos.html',
                {'usuarioproyecto':usuarioproyecto,'user':user}, RequestContext(request))


@login_required(login_url='/admin/login/')
def eliminar_proyecto(request, id_proyecto):
    proyecto= Proyecto.objects.get(pk=id_proyecto)
    user=request.user
    nombre=proyecto.nombre
    proyecto.delete()
    
    messages.success(request,"Proyecto "+nombre+" Eliminado!")
    return HttpResponseRedirect('/proyectos/')

 
    return render_to_response('HtmlProyecto/eliminarproyecto.html',{'proyecto':proyecto},
                             context_instance=RequestContext(request))

@login_required(login_url='/admin/login/')
def mis_proyectos(request):

    proyectos_list=Proyecto.objects.all()
    user=request.user

    return render_to_response('HtmlProyecto/misproyectos.html',{'proyectos':proyectos_list,'user':user})

@login_required(login_url='/admin/login/')
def mi_proyecto(request, id_proyecto):
 
    proyecto= Proyecto.objects.get(pk=id_proyecto)
    user=request.user
    permiso=RolUsuarioProyecto.objects.get(usuario_id=user, proyecto_id=id_proyecto)

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
                                   'id_proyecto':id_proyecto,'user':user,
                                   'permiso':permiso},context_instance=RequestContext(request))
    else:
        return render_to_response('HtmlProyecto/miproyecto.html',
                {'formulario':formulario,'proyecto':proyecto,
                 'id_proyecto':id_proyecto,'user':proyecto.scrumMaster},
                              context_instance=RequestContext(request))

@login_required(login_url='/admin/login/')
def listar_usuario_proyecto(request, id_proyecto):
    usuarioproyecto=RolUsuarioProyecto.objects.filter(proyecto_id=id_proyecto)
    proyecto=Proyecto.objects.get(pk=id_proyecto)

    return render_to_response('HtmlProyecto/lista_usuario_proyecto.html',{'usuarioproyecto':usuarioproyecto,
                                                                          'id_proyecto':id_proyecto, 'proyecto':proyecto},
                              context_instance=RequestContext(request))

@login_required(login_url='/admin/login/')
def asignar_usuario_proyecto(request, id_proyecto,id_user):

    usuarioproyecto=RolUsuarioProyecto()
    usuarioproyecto.proyecto_id=id_proyecto
    usuarioproyecto.usuario_id=id_user
    usuarioproyecto.save()
    messages.success(request, 'USUARIO ASIGNADO AL PROYECTO CORRECTAMENTE!')
    return HttpResponseRedirect('/proyecto/usuarios/'+str(id_proyecto))


@login_required(login_url='/admin/login/')
def listar_usuarios_para_asignar_proyecto(request, id_proyecto):
    lista=[]
    usuarioproyecto=RolUsuarioProyecto.objects.filter(proyecto_id=id_proyecto)
    usuarios=User.objects.all()
    user=request.user
    for user in usuarios:
        ban=1
        for user2 in usuarioproyecto:
            if user2.usuario.id == user.id: #si existe un usurio ya en tabla no quiero
                ban=0
        if ban == 1:
            lista.append(user)
    return render_to_response('HtmlProyecto/usuarios_asignar_proyecto.html',{'lista':lista,'usuarioproyecto':usuarioproyecto,
                                                                             'id_proyecto':id_proyecto,'user':user},
                              context_instance=RequestContext(request))


@login_required(login_url='/admin/login/')
def desasignar_usuario_proyecto(request, id_proyecto,id_user):

    usuarioproyecto=RolUsuarioProyecto.objects.get(usuario_id=id_user, proyecto_id=id_proyecto)
    usuarioproyecto.delete()
    messages.success(request, 'USUARIO DESASIGNADO AL PROYECTO CORRECTAMENTE!')
    return HttpResponseRedirect('/proyecto/usuarios/'+str(id_proyecto))


@login_required(login_url='/admin/login/')
def listar_roles_para_asignar_usuario(request, id_proyecto):
    roles=Group.objects.all()
    usuarioproyecto=RolUsuarioProyecto.objects.filter(proyecto_id=id_proyecto)

    return render_to_response('HtmlProyecto/usuarios_asignar_proyecto.html',{'roles':roles,'usuarioproyecto':usuarioproyecto,
                                                                             'id_proyecto':id_proyecto},
                              context_instance=RequestContext(request))

(MON, TUE, WED, THU, FRI, SAT, SUN) = range(7)

def fecha_calcular(start, days, holidays=(), workdays=(MON,TUE,WED,THU,FRI)):
    weeks, days = divmod(days, len(workdays))
    result = start + timedelta(weeks=weeks)
    lo, hi = min(start, result), max(start, result)
    count = len([h for h in holidays if h >= lo and h <= hi])
    days += count * (-1 if days < 0 else 1)
    for _ in range(days):
        result += timedelta(days=1)
        while result in holidays or result.weekday() not in workdays:
            result += timedelta(days=1)
    return result