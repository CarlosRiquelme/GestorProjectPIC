from mx.DateTime.DateTime import today
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from Actividades.models import Actividad
from AdminProyectos.models import Proyecto
from UserStory.models import UserStory
from django.contrib import messages
from Sprint.models import Sprint
from Comentario.models import Comentario
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from datetime import datetime, date, time, timedelta
from django.template.loader import render_to_string
from Sprint.models import Estimacion_Proyecto, Estimacion_Sprint
from matplotlib import pylab
from pylab import *
import PIL
import PIL.Image
import StringIO
from django.template import RequestContext, loader
from django.http import HttpResponse

def kanban(request,id_proyecto):
    actividades=Actividad.objects.filter(proyecto_id=id_proyecto).order_by("secuencia")
    userstorys=UserStory.objects.filter(proyecto_id=id_proyecto).order_by("estado")
    proyecto=Proyecto.objects.get(pk=id_proyecto)
    sprints=Sprint.objects.filter(proyecto_id=id_proyecto)

    return render_to_response('HtmlProyectoDesarrollo/kanban.html',{'actividades':actividades,
                                                                    'userstorys':userstorys,'proyecto':proyecto,
                                                                    'sprints':sprints, 'id_proyecto':id_proyecto})


def analizar_sprint(request, id_proyecto):

    sprint=Sprint.objects.get(proyecto_id=id_proyecto ,estado='ABIERTO')
    sprints=Sprint.objects.filter(proyecto_id=id_proyecto)
    ultimo_sprint=0
    for dato in sprints:
        if dato.secuencia > ultimo_sprint:
            ultimo_sprint=dato.secuencia
    if sprint.dias_duracion >= 1:
        sprint.dias_duracion=sprint.dias_duracion-1
        sprint.dia_trancurrido=sprint.dia_trancurrido+1
        suma=0.0
        resultado=0.0
        fraccion=0.0
        contador=0
        userstorys=UserStory.objects.filter(sprint_id=sprint.id)
        numerador=8*sprint.dia_trancurrido
        for dato in userstorys:
            denominador=dato.tiempo_estimado
            if denominador >= numerador:
                contador+=1
                fraccion=numerador/denominador
                suma+=fraccion
        resultado=(suma/contador)*100
        sprint.porcentaje_actual=resultado
        suma=0.0
        resultado=0.0
        contador=0
        for dato in userstorys:
            suma+=dato.porcentaje
            contador+=1
        resultado=(suma/contador)
        sprint.porcentaje_hecho_actual=resultado
        if sprint.dias_duracion == 0:
            sprint.estado='CERRADO'
            id_sprint=sprint.id
            siguiente=sprint.secuencia+1
            sprint.save()
            proyecto=Proyecto.objects.get(pk=id_proyecto)
            html_content = 'Su Proyecto   "'+proyecto.nombre+'"  a finalizado un Sprint Favor Fijarce si han terminados todos su user story"'
            send_mail('Finalizacion de Sprint',html_content , 'gestorprojectpic@gmail.com', [proyecto.scrumMaster.email], fail_silently=False)

            userstory2=UserStory.objects.filter(sprint_id=id_sprint)
            for dato in userstory2:
                if dato.porcentaje < 100:
                    dato.estado='REASIGNAR_SPRINT'
                    valor=100-dato.porcentaje
                    tiempo=0.0
                    tiempo_nuevo=0
                    tiempo=dato.tiempo_estimado*(valor/100)
                    tiempo=tiempo//8
                    tiempo_nuevo-=int(tiempo)
                    tiempo_nuevo+=1
                    dato.tiempo_estimado=tiempo_nuevo*8
                    dato.save()
            if siguiente <= ultimo_sprint:
                sprint2=Sprint.objects.get(proyecto_id=id_proyecto, secuencia=siguiente)
                sprint2.estado='ABIERTO'
                sprint2.save()
            else:
                #ACA SE CIERRA EL PROYECTO YA NO HAY MAS SPRINT EN LA LISTA POR ENDE TERMINA EL PROYECTO
                html_content = 'Su Proyecto   "'+proyecto.nombre+'"  a finalizado todos sus Sprint   "'
                send_mail('Finalizacion de todos sus Sprint',html_content , 'gestorprojectpic@gmail.com', [proyecto.scrumMaster.email], fail_silently=False)
                print "hacer algo como cerrar proyecto notificar scrumMaster"


        else:
            sprint.save()
    return HttpResponseRedirect('/proyecto/miproyecto/'+str(id_proyecto))

def visualizar_sprint_en_desarrollo(request,id_proyecto):
    sprints=Sprint.objects.filter(proyecto_id=id_proyecto)
    proyecto=Proyecto.objects.get(pk=id_proyecto)
    return render_to_response('HtmlProyectoDesarrollo/vizualizar_sprint.html',{'sprints':sprints,
                                                                               'id_proyecto':id_proyecto,
                                                                               'proyecto':proyecto})


def lista_reasignar_userstory_a_actividad(request,id_proyecto):
    userstorys=UserStory.objects.filter(proyecto_id=id_proyecto,estado='DONE')
    proyecto=Proyecto.objects.get(pk=id_proyecto)

    return render_to_response('HtmlProyectoDesarrollo/reasignar_userstory_actividad.html',{'userstorys':userstorys,
                                                                               'id_proyecto':id_proyecto,
                                                                               'proyecto':proyecto})
def reasignar_userstory_a_actividad(request,id_proyecto,id_userstory):
    userstory=UserStory.objects.get(pk=id_userstory)
    secuencia2=userstory.actividad.secuencia+1
    actividad=Actividad.objects.get(proyecto_id=id_proyecto,secuencia=secuencia2)
    userstory.actividad_id=actividad.id
    userstory.estado='TODO'
    userstory.save()
    messages.success(request, 'UserStory Reasignado a la Actividad Siguiente')
    return HttpResponseRedirect('/userstory/lista/actividad/reasignar/'+str(id_proyecto))

def lista_reasignar_userstory_a_sprint(request,id_proyecto):
    userstorys=UserStory.objects.filter(proyecto_id=id_proyecto,estado='REASIGNAR_SPRINT')
    proyecto=Proyecto.objects.get(pk=id_proyecto)
    return render_to_response('HtmlProyectoDesarrollo/reasignar_userstory_sprint.html',{'userstorys':userstorys,
                                                                               'id_proyecto':id_proyecto,
                                                                               'proyecto':proyecto})
def reasignar_userstory_a_sprint(request,id_proyecto,id_userstory):
    userstory=UserStory.objects.get(pk=id_userstory)
    secuencia2=userstory.sprint.secuencia+1
    sprint=Actividad.objects.get(proyecto_id=id_proyecto,secuencia=secuencia2)
    userstory.sprint_id=sprint.id
    userstory.estado='TODO'
    userstory.save()
    messages.success(request, 'UserStory Reasignado al Sprint Siguiente')
    return HttpResponseRedirect('/userstory/lista/sprint/reasignar/'+str(id_proyecto))

def cancelar_userstory(request,id_proyecto,id_userstory):
    userstory=UserStory.objects.get(pk=id_userstory)
    userstory.estado='CANCELADO'
    userstory.save()
    messages.success(request, 'UserStory CANCELADO!!!')
    return HttpResponseRedirect('/userstory/lista/actividad/reasignar/'+str(id_proyecto))

def scrumMaster(request, id_proyecto):
    user=request.user
    return render_to_response('HtmlProyectoDesarrollo/scrumMaster.html',{'user':user,
                                                                               'id_proyecto':id_proyecto })
def Burndowncharts(request, id_proyecto):
    x=[]
    y=[]
    sprint=[]
    estimacion_sprint=Estimacion_Sprint.objects.filter(proyecto_id=id_proyecto)
    suma=0
    for dato in estimacion_sprint:
        sprint.append(dato.duracion)
    for dato in sprint:
        x.append(suma)
        suma=suma+dato
    x.append(suma)
    resta=suma
    for i in sprint:
        y.append(resta)
        resta=resta-i
    y.append(0)
    plot(x,y,linewidth=2)

    xlabel('x axis')
    ylabel('y axis')
    title('sample graph')
    grid(True)
    pylab.show()

    buffer = StringIO.StringIO()
    canvas = pylab.get_current_fig_manager().canvas
    canvas.draw()
    graphIMG = PIL.Image.fromstring("RGB",canvas.get_width_height(), canvas.tostring_rgb())
    graphIMG.save(buffer,"PNG")
    pylab.close()

    return HttpResponse(buffer.getvalue(), content_type="image/png")


