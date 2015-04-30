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
from django.contrib.auth.decorators import login_required



def nueva_actividad(request):
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
            fecha_inicio = actividad_form.cleaned_data['fechaInicio']
            fechafin=actividad_form.cleaned_data['fechaFin']
            flujo =  actividad_form.cleaned_data['flujo']
            secuencia = actividad_form.cleaned_data['secuencia']




            actividad = Actividad()
            actividad.nombre=nombre
            actividad.flujo=flujo
            actividad.fecha_creacion=today()
            actividad.fechaInicio=fecha_inicio
            actividad.fechaFin=fechafin
            actividad.estado='PROGRAMADO'
            actividad.secuencia = secuencia
            actividad.save()
            messages.success(request, 'actividad CREADO CON EXITO!')


            #aux = Rol.objects.filter(nombre='Leader').count()
            #===================================================================
            # if aux == 0:
            #    rol= crearRolLeader()
            # else:
            #     rol = Rol.objects.get(nombre='Leader')
            # rol_user=RolUser()
            # rol_user.rol = rol
            # rol_user.actividad = actividad
            # rol_user.user = user
            # rol_user.save()
            #===================================================================
            return HttpResponseRedirect('/actividad/miactividad/'+str(actividad.id))
    else:
        actividad_form= ActividadForm(request.POST)
    return render_to_response('HtmlActividad/nueva_actividad.html',{'formulario':actividad_form,'user':user},
                              context_instance=RequestContext(request))
