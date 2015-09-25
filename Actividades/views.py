 # coding=UTF-8
from mx.DateTime.DateTime import today
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from Actividades.forms import ActividadForm, EditActividadForm
from Actividades.models import Actividad
from django.contrib import messages
from UserStory.models import UserStory
from AdminProyectos.models import Proyecto
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

@login_required(login_url='/admin/login/')
def nueva_actividad(request, id_proyecto):

    """
    Crea un nuevo actividad dentro del Proyecto

    """
    user=request.user
    actividad_ultima=Actividad.objects.filter(proyecto_id=id_proyecto)
    ultimo=0
    for object in actividad_ultima:
        if ultimo <= object.secuencia:
            ultimo = object.secuencia
    if request.method=='POST':
        actividad_form = ActividadForm(data=request.POST)
        # If the two forms are valid...
        if actividad_form.is_valid():
            actividad_form.clean()
            nombre = actividad_form.cleaned_data['nombre']
            actividad = Actividad()
            actividad.nombre=nombre
            actividad.proyecto_id=id_proyecto
            actividad.fecha_creacion=today()
            actividad.secuencia = ultimo+1
            actividad.save()
            messages.success(request, 'actividad CREADO CON EXITO!')

            return HttpResponseRedirect('/actividad/miactividad/'+str(actividad.id))
    else:
        actividad_form= ActividadForm(request.POST)
    return render_to_response('HtmlActividad/nueva_actividad.html',{'formulario':actividad_form,'user':user,'id_proyecto':id_proyecto},
                              context_instance=RequestContext(request))
@login_required(login_url='/admin/login/')
def editar_actividad(request,id_proyecto, id_actividad):
    """
    Edita los atributos de una Actividad
    :param request:
    :param id_proyecto:
    :param id_actividad:
    :return:
    """

    user=request.user
    actividad=Actividad.objects.get(pk=id_actividad)
    if request.method=='POST':
       formulario =EditActividadForm(request.POST,instance=actividad)
       if formulario.is_valid():
           formulario.save()
           messages.success(request,"Actividad modificada con exito!")
           return HttpResponseRedirect('/actividad/misactividades/'+str(id_proyecto))
       else:
           messages.warning(request,"Debe completar los campos obligatorios!")
    else:
       formulario = EditActividadForm(instance=actividad)
    return render_to_response('HtmlActividad/editaractividad.html',{'formulario':formulario,
                                                                     'id_proyecto':id_proyecto}, context_instance=RequestContext(request))

@login_required(login_url='/admin/login/')
def eliminar_actividad(request, id_proyecto , id_actividad):
    """
    Elimina una Actividad
    :param request:
    :param id_proyecto:
    :param id_actividad:
    :return:
    """
    actividad= Actividad.objects.get(pk=id_actividad)
    user=request.user
    nombre=actividad.nombre
    actividad.delete()

    messages.success(request,"Activadad "+nombre+" Eliminada!")
    return HttpResponseRedirect('/actividad/misactividades/'+str(id_proyecto))

@login_required(login_url='/admin/login/')
def pre_eliminar_actividad(request, id_proyecto, id_actividad):
    """
    Funcion que se invoca para aprobar la Eliminacion de la Actividad
    :param request:
    :param id_proyecto:
    :param id_actividad:
    :return:
    """
    user=request.user
    proyecto=Proyecto.objects.get(pk=id_proyecto)
    actividad=Actividad.objects.get(pk=id_actividad)
    return render_to_response('HtmlActividad/eliminaractividad.html',{'actividad':actividad,
                                                                    'user':user,
                                                                    'proyecto':proyecto},
                             context_instance=RequestContext(request))
@login_required(login_url='/admin/login/')
def mi_actividad(request, id_actividad):
    """
    Funcion que muestra los atributos de la Actividad
    :param request:
    :param id_actividad:
    :return:
    """

    actividad= Actividad.objects.get(pk=id_actividad)
    user=request.user

    return render_to_response('HtmlActividad/miactividad.html',
                { 'actividad':actividad, 'user':user}, RequestContext(request))


@login_required(login_url='/admin/login/')
def mis_actividades(request, id_proyecto):
    """
    Lista todas las actividades de un Proyecto
    :param request:
    :param id_proyecto:
    :return:
    """

    actividades=Actividad.objects.filter(proyecto_id=id_proyecto).order_by('secuencia')
    user=request.user
    proyecto=Proyecto.objects.get(pk=id_proyecto)
    paginator=Paginator(actividades,10)
    page=request.GET.get('page')
    try:
        actividades=paginator.page(page)
    except PageNotAnInteger:
        actividades=paginator.page(1)
    except EmptyPage:
        actividades=paginator.page(paginator.num_pages)



    return render_to_response('HtmlActividad/misactividades.html',{'actividades':actividades, 'id_proyecto':id_proyecto,
                                                                   'user':user,'proyecto':proyecto})

@login_required(login_url='/admin/login/')
def ver_estados(request, id_proyecto, id_actividad):
    """
    Muestar los distintos estados de una actividad
    :param request:
    :param id_proyecto:
    :param id_actividad:
    :return:
    """
    actividad=Actividad.objects.get(pk=id_actividad)

    return render_to_response('HtmlActividad/estados.html',{ 'id_proyecto':id_proyecto, 'id_actividad':id_actividad,
                                                             'actividad':actividad})

