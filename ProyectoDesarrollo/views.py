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
#from matplotlib import pylab
#import matplotlib.pyplot
#from pylab import *
#import PIL
#import PIL.Image
#import StringIO
from django.template import RequestContext, loader
from django.http import HttpResponse
from Sprint.models import Sprint_En_Proceso,Dias_de_un_Sprint

def kanban(request,id_proyecto):
    actividades=Actividad.objects.filter(proyecto_id=id_proyecto).order_by("secuencia")
    userstorys=UserStory.objects.filter(proyecto_id=id_proyecto).order_by("estado")
    proyecto=Proyecto.objects.get(pk=id_proyecto)
    sprints=Sprint.objects.filter(proyecto_id=id_proyecto)

    return render_to_response('HtmlProyectoDesarrollo/kanban.html',{'actividades':actividades,
                                                                    'userstorys':userstorys,'proyecto':proyecto,
                                                                    'sprints':sprints, 'id_proyecto':id_proyecto})


def analizar_sprint(request, id_proyecto):
    """
    Se analiza el sprint en la fecha actual se guardan los datos de los user story del sprint hasta la fecha
    si hay mas de una consulta por dia solo se registra uno por dia
    :param request:
    :param id_proyecto:
    :return:
    """
    sprint=Sprint.objects.get(proyecto_id=id_proyecto ,estado='ABIERTO')
    sprints=Sprint.objects.filter(proyecto_id=id_proyecto)
    sprint_fechas=Dias_de_un_Sprint.objects.filter(sprint_id=sprint.id)
    ultimo_sprint=0
    proyecto=Proyecto.objects.get(pk=id_proyecto)
    for dato in sprints:
        if dato.secuencia > ultimo_sprint:
            ultimo_sprint=dato.secuencia

    fecha_actual_sprint=date.today()
    userstorys=UserStory.objects.filter(sprint_id=sprint.id)
    suma=0
    for dato2 in userstorys:
        suma+=dato2.tiempo_trabajado
    for dato in sprint_fechas:
        sprint_en_proceso1=Sprint_En_Proceso.objects.get(fecha=fecha_actual_sprint)
        if fecha_actual_sprint == dato.fecha:
            if sprint_en_proceso1 == 'NULL':
                sprint_en_proceso=Sprint_En_Proceso()
                sprint_en_proceso.sprint_id=sprint.id
                sprint_en_proceso.fecha=fecha_actual_sprint
                sprint_en_proceso.horas_acumulada=suma
                sprint_en_proceso.save()
            else:
                sprint_en_proceso1.horas_acumulada=suma
                sprint_en_proceso1.save()
    if fecha_actual_sprint == sprint.fechaFin:
        hora=time.strftime("%X")
        hora2= '19:00:00'
        if hora < hora2:
            print "Horaaaaaaaaaaaaaa " + hora
        else:
            sprint.estado='CERRADO'
            id_sprint=sprint.id
            siguiente=sprint.secuencia+1
            sprint.save()
            html_content = 'Su Proyecto   "'+proyecto.nombre+'"  a finalizado un Sprint Favor Fijarce si han terminados todos su user story"'
            send_mail('Finalizacion de Sprint',html_content , 'gestorprojectpic@gmail.com', [proyecto.scrumMaster.email], fail_silently=False)
            userstory2=UserStory.objects.filter(sprint_id=id_sprint)
            ban=0
            for dato in userstory2:
                if dato.estado != 'DONE' and dato.estado != 'FINALIZADO' and dato.estado != 'CANCELADO' :
                    dato.estado='REASIGNAR_SPRINT'
                    dato.save()
                    ban=1
            if siguiente <= ultimo_sprint:
                sprint2=Sprint.objects.get(proyecto_id=id_proyecto, secuencia=siguiente)
                sprint2.estado='ABIERTO'
                sprint2.save()
            else:
                if ban == 1:
                    html_content = 'Su Proyecto   "'+proyecto.nombre+'"  a finalizado todos sus Sprint, pero quedan aun user storys sin concluir  "'
                    send_mail('Finalizacion de todos sus Sprint',html_content , 'gestorprojectpic@gmail.com', [proyecto.scrumMaster.email], fail_silently=False)
                    proyecto.estado='REVISAR'
                if ban == 0:
                    html_content = 'Su Proyecto   "'+proyecto.nombre+'"  a finalizado todos sus Sprint. Y sus user story estan todos Finalizados.   "'
                    send_mail('Finalizacion de todos sus Sprint',html_content , 'gestorprojectpic@gmail.com', [proyecto.scrumMaster.email], fail_silently=False)
                    proyecto.estado='REVISAR'





    return HttpResponseRedirect('/proyecto/miproyecto/'+str(id_proyecto))

def visualizar_sprint_en_desarrollo(request,id_proyecto):
    sprints=Sprint.objects.filter(proyecto_id=id_proyecto)
    proyecto=Proyecto.objects.get(pk=id_proyecto)
    return render_to_response('HtmlProyectoDesarrollo/vizualizar_sprint.html',{'sprints':sprints,
                                                                               'id_proyecto':id_proyecto,
                                                                               'proyecto':proyecto})


def lista_reasignar_userstory_a_actividad(request,id_proyecto):
    """
    Lista los user story que el SM debe aprobar y reasignar a la siguiente actividad
    :param request:
    :param id_proyecto:
    :return:
    """
    userstorys=UserStory.objects.filter(proyecto_id=id_proyecto,estado='REVISAR_FIN_AC')
    proyecto=Proyecto.objects.get(pk=id_proyecto)

    return render_to_response('HtmlProyectoDesarrollo/reasignar_userstory_actividad.html',{'userstorys':userstorys,
                                                                               'id_proyecto':id_proyecto,

                                                                               'proyecto':proyecto})
def reasignar_userstory_a_actividad(request,id_proyecto,id_userstory):

    """
    Reasigna el  User Story a la siguiente actividad
    :param request:
    :param id_proyecto:
    :param id_userstory:
    :return:
    """
    userstory=UserStory.objects.get(pk=id_userstory)
    actividad=Actividad.objects.filter(proyecto_id=id_proyecto)
    ultima_actividad=0
    secuencia2=0
    valor=0
    valor=userstory.actividad.secuencia
    for dato in actividad:
        if dato.secuencia > ultima_actividad:
            ultima_actividad=dato.secuencia

    if valor < ultima_actividad:
        secuencia2=valor+1
        actividad=Actividad.objects.get(proyecto_id=id_proyecto,secuencia=secuencia2)
        userstory.actividad_id=actividad.id
        userstory.estado='TODO'
        userstory.save()
        messages.success(request, 'UserStory Reasignado a la Actividad Siguiente')
        return HttpResponseRedirect('/userstory/lista/actividad/reasignar/'+str(id_proyecto))
    else:
        messages.success(request, 'El User Story ya se encuentra en la ultima Actividad del Proyecto')
        messages.success(request, 'NO se pueder reasignar la Actividad')
        return HttpResponseRedirect('/proyecto/scrumMaster/'+str(id_proyecto))

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


