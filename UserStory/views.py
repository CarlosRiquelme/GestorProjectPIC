# coding=UTF-8
from mx.DateTime.DateTime import today
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from UserStory.forms import UserStoryForm, UserStoryFormEdit
from UserStory.models import UserStory
from django.contrib import messages
from django.contrib.auth.decorators import login_required



def nuevo_userstory(request, id_proyecto):
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
            prioridad=userstory_form.cleaned_data['prioridad']




            userstory = UserStory()
            userstory.nombre=nombre
            userstory.descripcion = descripcion
            userstory.fecha_creacion=today()
            userstory.fechaInicio=fecha_inicio
            userstory.fechaFin=fechafin
            userstory.estado='CREADO'
            userstory.prioridad=prioridad
            userstory.tiempo_trabajado=tiempo_trabajado
            userstory.porcentaje=porcentaje
            userstory.proyecto_id=id_proyecto
            userstory.save()
            messages.success(request, 'USER STORY CREADO CON EXITO!')
                        


            return HttpResponseRedirect('/userstory/miuserstory/'+str(userstory.id))
    else:
        userstory_form= UserStoryForm(request.POST)
    return render_to_response('HtmlUserStory/nuevouserstory.html',{'formulario':userstory_form,'user':user,
                                                                   'id_proyecto':id_proyecto},
                              context_instance=RequestContext(request))


def iniciar_userstory(request, id_userstory):
    userstory= UserStory.objects.get(pk=id_userstory)
    userstory.estado='DOING'
    userstory.save()
    messages.success(request,'UserStory "'+userstory.nombre+'" doing')
    return HttpResponseRedirect('/userstory/miuserstory/'+str(id_userstory))

def editar_userstory(request, id_userstory):
 
    userstory= UserStory.objects.get(pk=id_userstory)
    user=request.user
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



def userstorys(request):
    userstory = UserStory.objects.all()


    return render_to_response('HtmlUserStory/userstorys.html',
                {'userstory':userstory}, RequestContext(request))



def eliminar_userstory(request, id_userstory):
    userstory= UserStory.objects.get(pk=id_userstory)
    user=request.user
    nombre=userstory.nombre
    userstory.delete()
    
    messages.success(request,"UserStory "+nombre+" Eliminado!")
    return HttpResponseRedirect('/userstorys/')

 
    return render_to_response('HtmlUserStory/eliminaruserstory.html',{'userstory':userstory},
                              context_instance=RequestContext(request))
def mis_userstorys(request, id_proyecto):
    userstorys=UserStory.objects.filter(proyecto_id=id_proyecto)

    return render_to_response('HtmlUserStory/misuserstorys.html',{'userstorys':userstorys,'id_proyecto':id_proyecto})


def mi_userstory(request, id_userstory):

    userstory= UserStory.objects.get(pk=id_userstory)
    user=request.user

    return render_to_response('HtmlUserStory/miuserstory.html',
                { 'userstory':userstory }, RequestContext(request))
# def asinar_userstory_a_actividad(request,id_actividad,id_proyecto):
#     userstorys=UserStory.objects.filter(proyecto_id=id_proyecto)


