 # coding=UTF-8
from mx.DateTime.DateTime import today
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from Actividades.forms import ActividadForm
from Actividades.models import Actividad
from django.contrib import messages
from UserStory.models import UserStory
from AdminProyectos.models import Proyecto
from django.contrib.auth.decorators import login_required



def nueva_actividad(request, id_proyecto):
    """
    Crea un nuevo actividad
    """
    user=request.user
    #if not user.is_staff:
     #   return HttpResponseRedirect('/sinpermiso')
    if request.method=='POST':
        actividad_form = ActividadForm(data=request.POST)


        # If the two forms are valid...
        if actividad_form.is_valid():
            # Guarda el Usuarios en la bd
            actividad_form.clean()
            nombre = actividad_form.cleaned_data['nombre']
            secuencia = actividad_form.cleaned_data['secuencia']




            actividad = Actividad()
            actividad.nombre=nombre
            actividad.proyecto_id=id_proyecto
            actividad.fecha_creacion=today()
            actividad.secuencia = secuencia
            actividad.save()
            messages.success(request, 'actividad CREADO CON EXITO!')

            return HttpResponseRedirect('/actividad/miactividad/'+str(actividad.id))
    else:
        actividad_form= ActividadForm(request.POST)
    return render_to_response('HtmlActividad/nueva_actividad.html',{'formulario':actividad_form,'user':user,'id_proyecto':id_proyecto},
                              context_instance=RequestContext(request))


def mi_actividad(request, id_actividad):

    actividad= Actividad.objects.get(pk=id_actividad)
    user=request.user

    return render_to_response('HtmlActividad/miactividad.html',
                { 'actividad':actividad, 'user':user}, RequestContext(request))



def mis_actividades(request, id_proyecto):

    actividades=Actividad.objects.filter(proyecto_id=id_proyecto)
    user=request.user
    proyecto=Proyecto.objects.get(pk=id_proyecto)



    return render_to_response('HtmlActividad/misactividades.html',{'actividades':actividades, 'id_proyecto':id_proyecto,
                                                                   'user':user,'proyecto':proyecto})


def ver_estados(request, id_proyecto, id_actividad):
    actividad=Actividad.objects.get(pk=id_actividad)

    return render_to_response('HtmlActividad/estados.html',{ 'id_proyecto':id_proyecto, 'id_actividad':id_actividad,
                                                             'actividad':actividad})

