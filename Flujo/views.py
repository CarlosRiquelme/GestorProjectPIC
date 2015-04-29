 # coding=UTF-8
from mx.DateTime.DateTime import today
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from Flujo.forms import FlujoForm
from Flujo.models import Flujo
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def nuevo_flujo(request):
    """
    Crea un nuevo proyecto
    """
    user=request.user
    #if not user.is_staff:
     #   return HttpResponseRedirect('/sinpermiso')
    if request.method=='POST':
        flujo_form = FlujoForm(data=request.POST)


        # If the two forms are valid...
        if flujo_form.is_valid():
            # Guarda el Usuarios en la bd
            flujo_form.clean()
            nombre = flujo_form.cleaned_data['nombre']
            proyecto = flujo_form.cleaned_data['proyecto']
            cantidad_de_actividades = flujo_form.cleaned_data['cantidad_de_actividades']



            flujo = Flujo()
            flujo.nombre=nombre
            flujo.proyecto=proyecto
            flujo.cantidad_de_actividades=cantidad_de_actividades
            flujo.fecha_creacion=today()
            flujo.save()
            messages.success(request, 'FLUJO CREADO CON EXITO!')

            return HttpResponseRedirect('/flujo/miflujo/'+str(flujo.id))
    else:
        flujo_form= FlujoForm(request.POST)
    return render_to_response('HtmlFlujo/nuevoflujo.html',{'formulario':flujo_form,'user':user},
                              context_instance=RequestContext(request))
