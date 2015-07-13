from mx.DateTime.DateTime import today
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from ProyectoDesarrollo.forms import UserStoryFormTiempo
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from Actividades.models import Actividad
from AdminProyectos.models import Proyecto
from UserStory.models import UserStory, US_Estado_ultimo
from django.contrib import messages
from Sprint.models import Sprint
from Comentario.models import Comentario
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from datetime import datetime, date, time, timedelta
import time
from time import strftime
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
from django.core.exceptions import ObjectDoesNotExist

def kanban(request,id_proyecto):
    actividades=Actividad.objects.filter(proyecto_id=id_proyecto).order_by("secuencia")
    userstorys=UserStory.objects.filter(proyecto_id=id_proyecto).order_by("estado")
    userstorys2=UserStory.objects.filter(proyecto_id=id_proyecto, estado='REASIGNAR_SPRINT')
    lista=[]
    for dato in userstorys2:
        bandera=True
        try:
            us_estado_ultimo=US_Estado_ultimo.objects.get(us_id=dato.id)
        except ObjectDoesNotExist:
            bandera=False
        if bandera == True:
            lista.append(us_estado_ultimo)
    proyecto=Proyecto.objects.get(pk=id_proyecto)
    sprints=Sprint.objects.filter(proyecto_id=id_proyecto)

    return render_to_response('HtmlProyectoDesarrollo/kanban.html',{'actividades':actividades,
                                                                    'userstorys':userstorys,'proyecto':proyecto,
                                                                    'sprints':sprints, 'id_proyecto':id_proyecto,
                                                                    'lista':lista})


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
    ultima_actividad=0
    proyecto=Proyecto.objects.get(pk=id_proyecto)
    actividad=Actividad.objects.filter(proyecto_id=id_proyecto)
    for dato in sprints:
        if dato.secuencia > ultimo_sprint:
            ultimo_sprint=dato.secuencia
    for dato in actividad:
        if dato.secuencia > ultima_actividad:
            ultima_actividad=dato.secuencia

    fecha_actual_sprint=date.today()
    userstorys=UserStory.objects.filter(sprint_id=sprint.id)
    suma=0
    for dato2 in userstorys:
        suma+=dato2.tiempo_trabajado
    for dato in sprint_fechas:
        bandera=True
        try:
            sprint_en_proceso=Sprint_En_Proceso.objects.get(sprint_id=sprint.id, fecha=fecha_actual_sprint)
        except ObjectDoesNotExist:
            bandera=False
        if fecha_actual_sprint == dato.fecha:
            if bandera == False:
                sprint_en_proceso=Sprint_En_Proceso()
                sprint_en_proceso.sprint_id=sprint.id
                sprint_en_proceso.fecha=fecha_actual_sprint
                sprint_en_proceso.horas_acumulada=suma
                sprint_en_proceso.save()
            if bandera == True:
                sprint_en_proceso.horas_acumulada=suma
                sprint_en_proceso.save()
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
            html_content = 'Su Proyecto   "'+proyecto.nombre+'"  a finalizado un Sprint Favor Fijarse si han terminados todos su user story"'
            send_mail('Finalizacion de Sprint',html_content , 'gestorprojectpic@gmail.com', [proyecto.scrumMaster.email], fail_silently=False)
            userstory2=UserStory.objects.filter(sprint_id=id_sprint)
            ban=0
            for dato in userstory2:
                bandera=True
                try:
                    us_estado_ultimo=US_Estado_ultimo.objects.get(us_id=dato.id)
                except ObjectDoesNotExist:
                    bandera=False

                if dato.actividad.secuencia == ultima_actividad:
                    if dato.estado != 'DONE' and dato.estado != 'FINALIZADO' and dato.estado != 'CANCELADO' :
                        if bandera == False:
                            us_estado_ultimo=US_Estado_ultimo()
                            us_estado_ultimo.us_id=dato.id
                            us_estado_ultimo.estado=dato.estado
                            us_estado_ultimo.estado_actual='REASIGNAR_SPRINT'
                            us_estado_ultimo.save()
                        if bandera == True:
                            us_estado_ultimo.estado=dato.estado
                            us_estado_ultimo.estado_actual='REASIGNAR_SPRINT'
                            us_estado_ultimo.save()
                        dato.estado='REASIGNAR_SPRINT'
                        dato.save()
                        ban=1
                else:
                    if  dato.estado != 'FINALIZADO' and dato.estado != 'CANCELADO' :
                        if bandera == False:
                            us_estado_ultimo=US_Estado_ultimo()
                            us_estado_ultimo.us_id=dato.id
                            us_estado_ultimo.estado=dato.estado
                            us_estado_ultimo.estado_actual='REASIGNAR_SPRINT'
                            us_estado_ultimo.save()
                        if bandera == True:
                            us_estado_ultimo.estado=dato.estado
                            us_estado_ultimo.estado_actual='REASIGNAR_SPRINT'
                            us_estado_ultimo.save()
                        dato.estado='REASIGNAR_SPRINT'
                        dato.save()
                        ban=1
            if siguiente <= ultimo_sprint:
                sprint2=Sprint.objects.get(proyecto_id=id_proyecto, secuencia=siguiente)
                sprint2.estado='ABIERTO'
                sprint2.save()
            else:
                if ban == 1:
                    html_content = 'Su Proyecto   "'+proyecto.nombre+'"  a finalizado todos sus Sprint, pero quedan aun user storys sin concluir se creo un nuevo Sprint donde se han ubicado todos su user storys sin terminar  "'
                    send_mail('Finalizacion de todos sus Sprint',html_content , 'gestorprojectpic@gmail.com', [proyecto.scrumMaster.email], fail_silently=False)
                    proyecto.estado='REVISAR'
                    crear_nuevo_sprint(id_proyecto)

                if ban == 0:
                    html_content = 'Su Proyecto   "'+proyecto.nombre+'"  a finalizado todos sus Sprint. Y sus user story estan todos Finalizados.   "'
                    send_mail('Finalizacion de todos sus Sprint',html_content , 'gestorprojectpic@gmail.com', [proyecto.scrumMaster.email], fail_silently=False)
                    proyecto.estado='REVISAR'





    return HttpResponseRedirect('/proyecto/sprint/visualizar/'+str(id_proyecto))


def crear_nuevo_sprint(id_proyecto):
    sprint=Sprint.objects.filter(proyecto_id=id_proyecto)
    proyecto=Proyecto.objects.get(pk=id_proyecto)
    userstory=UserStory.objects.filter(proyecto_id=id_proyecto, estado='REASIGNAR_SPRINT')
    mayor_tiempo=0
    resta=0
    valor=0
    for dato in userstory:
        resta=dato.tiempo_estimado-dato.tiempo_trabajado
        if resta > mayor_tiempo:
            mayor_tiempo=resta
    valor=int(mayor_tiempo/8)+1
    ultimo_sprint=0
    ahora = date.today()
    siguiente=0
    for dato in sprint:
        if ultimo_sprint < dato.secuencia:
            ultimo_sprint=dato.secuencia
    sprint2=Sprint.objects.filter(proyecto_id=id_proyecto,secuencia=ultimo_sprint)
    fecha1=sprint2.fechaInicio
    siguiente=ultimo_sprint+1
    nombre= 'Sprint_Recuperacion_'+str(siguiente)
    sprint_nuevo=Sprint()
    sprint_nuevo.nombre=nombre
    sprint_nuevo.secuencia=siguiente
    sprint_nuevo.estado='ABIERTO'
    sprint_nuevo.fecha_creacion=ahora
    sprint_nuevo.fechaInicio=fecha_calcular(fecha1,1)
    sprint_nuevo.fechaFin=fecha_calcular(sprint_nuevo.fechaInicio,valor)
    sprint_nuevo.proyecto_id=id_proyecto
    sprint_nuevo.tiempo_acumulado=valor*8
    sprint_nuevo.dia_trancurrido=0
    sprint_nuevo.dias_duracion=valor
    sprint_nuevo.suma_tiempo_usestory=0
    sprint_nuevo.save()
    sprint3=Sprint.objects.get(proyecto_id=id_proyecto,estado='ABIERTO')
    for dato in userstory:
        us_estado_ultimo=US_Estado_ultimo.objects.get(us_id=dato.id, estado_actual='REASIGNAR_SPRINT')
        dato.sprint_id=sprint3.id
        dato.tiempo_estimado=mayor_tiempo
        dato.estado=us_estado_ultimo.estado
        dato.save()


def visualizar_sprint_en_desarrollo(request,id_proyecto):
    proyecto=Proyecto.objects.get(pk=id_proyecto)
    ahora = date.today()
    sprints=Sprint.objects.filter(proyecto_id=id_proyecto)
    ultimo_sprint=0
    for dato in sprints:
        if ultimo_sprint < dato.secuencia:
            ultimo_sprint=dato.secuencia
    try:
        sprint=Sprint.objects.get(proyecto_id=id_proyecto, estado='ABIERTO')
    except ObjectDoesNotExist:
        sprint=Sprint.objects.get(proyecto_id=id_proyecto, secuencia=ultimo_sprint)
    userstorys=UserStory.objects.filter(sprint_id=sprint.id)
    suma=0
    ahora = date.today()
    contador=0
    for dato in userstorys:
        suma+=dato.tiempo_trabajado
        contador+=1

    estimacion_sprint=Estimacion_Sprint.objects.get(sprint_id=sprint.id)
    bandera=True
    try:
        sprint_en_proceso=Sprint_En_Proceso.objects.get(sprint_id=sprint.id, fecha=ahora)
    except ObjectDoesNotExist:
        bandera=False
    if bandera == False:
        print "holaaaaaaaaaaaaaaaa"
        sprint_en_proceso=Sprint_En_Proceso()
        sprint_en_proceso.sprint_id=sprint.id
        sprint_en_proceso.fecha=ahora
        sprint_en_proceso.horas_acumulada=suma
        sprint_en_proceso.save()
    if bandera == True:
        print "holaaaaaaaaaaaaaaa222222222222"
        sprint_en_proceso.horas_acumulada=suma
        sprint_en_proceso.fecha=ahora
        sprint_en_proceso.save()

    sprints=Sprint.objects.filter(proyecto_id=id_proyecto).order_by('secuencia')
    lista_sprint_proceso=[]
    lista_estimacion_sprint=[]
    lista_porcentaje=[]
    total_horas=0
    for dato in sprints:
        userstorys1=UserStory.objects.filter(proyecto_id=id_proyecto, sprint_id=dato.id)
        for dato1 in userstorys1:
            total_horas+=dato1.tiempo_estimado
    lista_porcentaje_estimado=[]
    lista_hora_estimado=[]
    lista_hora_proceso=[]
    valor=0
    for dato in sprints:
        porcentaje_sprint_hecho=0.0
        bandera=True
        try:
            sprint_proceso=Sprint_En_Proceso.objects.get(sprint_id=dato.id, fecha=ahora)
        except ObjectDoesNotExist:
            bandera=False
        if bandera == True:
            porcentaje_sprint_hecho=sprint_en_proceso.horas_acumulada*100/total_horas
            lista_sprint_proceso.append(sprint_proceso)
            lista_porcentaje.append(porcentaje_sprint_hecho)
            lista_hora_proceso.append(sprint_proceso.horas_acumulada)
        sprint_estimacion=Estimacion_Sprint.objects.get(sprint_id=dato.id)
        lista_estimacion_sprint.append(sprint_estimacion)
        userstorys1=UserStory.objects.filter(proyecto_id=id_proyecto, sprint_id=dato.id)
        for dato1 in userstorys1:
            valor+=dato1.tiempo_estimado
        lista_porcentaje_estimado.append(valor*100/total_horas)
        lista_hora_estimado.append(valor)

    return render_to_response('HtmlProyectoDesarrollo/vizualizar_sprint.html',{'sprints':sprints,
                                                                               'id_proyecto':id_proyecto,
                                                                               'proyecto':proyecto,
                                                                               'lista_sprint_proceso':lista_sprint_proceso,
                                                                               'lista_estimacion_sprint':lista_estimacion_sprint,
                                                                               'lista_porcentaje':lista_porcentaje,
                                                                               'lista_porcentaje_estimado':lista_porcentaje_estimado,
                                                                               'lista_hora_estimado':lista_hora_estimado,
                                                                               'lista_hora_proceso':lista_hora_proceso})


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
    sprints=Sprint.objects.filter(proyecto_id=id_proyecto)
    bandera=True
    bandera2=True
    try:
        us_ultimo_estado=US_Estado_ultimo.objects.get(us_id=id_userstory, estado_actual='REASIGNAR_SPRINT')
    except ObjectDoesNotExist:
            bandera=False
    ultimo_sprint=0
    for dato in sprints:
        if dato.secuencia >= ultimo_sprint:
            ultimo_sprint=dato.secuencia
    try:
        sprint=Sprint.objects.get(proyecto_id=id_proyecto, estado='ABIERTO')
    except ObjectDoesNotExist:
        bandera2=False
    if bandera == True:
        if sprint.secuencia > ultimo_sprint:
            userstory.sprint_id=sprint.id
            userstory.estado=us_ultimo_estado.estado
            userstory.save()
        if sprint.secuencia == ultimo_sprint:
            print "hola"
    if bandera == False:
        if sprint.secuencia > ultimo_sprint:
            print "hola2"

    messages.success(request, 'UserStory Reasignado al Sprint Siguiente')
    return HttpResponseRedirect('/userstory/lista/sprint/reasignar/'+str(id_proyecto))



def scrumMaster(request, id_proyecto):
    user=request.user
    return render_to_response('HtmlProyectoDesarrollo/scrumMaster.html',{'user':user,
                                                                               'id_proyecto':id_proyecto })


def lista_reasignar_userstory_tiempo(request,id_proyecto):
    userstorys=UserStory.objects.filter(proyecto_id=id_proyecto,estado='REVISAR_TIEMPO')
    proyecto=Proyecto.objects.get(pk=id_proyecto)
    return render_to_response('HtmlProyectoDesarrollo/reasignar_userstory_tiempo.html',{'userstorys':userstorys,
                                                                               'id_proyecto':id_proyecto,
                                                                               'proyecto':proyecto})

def reasignar_userstory_tiempo(request,id_proyecto,id_userstory):
    userstory=UserStory.objects.get(pk=id_userstory)
    sprint=Sprint.objects.get(proyecto_id=id_proyecto, estado='ABIERTO')
    id_sprint=sprint.id
    user=request.user
    if request.method=='POST':
        formulario= UserStoryFormTiempo(request.POST,instance=userstory)
        if formulario.is_valid():
            userstory= formulario.save()
            completar_atributos_userstory_tiempo(id_userstory,id_sprint)
            messages.success(request,'UserStory "'+userstory.nombre+'" fue asignado su Nuevo TIEMPO')
            return HttpResponseRedirect('/userstory/miuserstory/'+str(id_userstory))
    else:
        formulario= UserStoryFormTiempo(instance=userstory)
    return render_to_response('HtmlUserStory/reasignar_tiempo.html',
                {'formulario':formulario,'id_userstory':id_userstory,
                 'id_proyecto':id_proyecto,
                 'userstory':userstory},
                              context_instance=RequestContext(request))




def completar_atributos_userstory_tiempo(id_userstory,id_sprint):
    userstory=UserStory.objects.get(pk=id_userstory)
    us_estado=US_Estado_ultimo.objects.get(us_id=id_userstory, estado_actual='REVISAR_TIEMPO')
    userstory.estado=us_estado.estado
    userstory.sprint_id=id_sprint
    userstory.save()



def lista_aprobacion_finalizacion(request, id_proyecto):
    userstory=UserStory.objects.filter(proyecto_id=id_proyecto, estado='REVISAR_FIN')
    proyecto=Proyecto.objects.get(pk=id_proyecto)
    actividades=Actividad.objects.filter(proyecto_id=id_proyecto)
    ultima_actividad=0
    lista=[]
    for dato in actividades:
        if ultima_actividad < dato.secuencia:
            ultima_actividad=dato.secuencia
    for dato in userstory:
        if dato.actividad.secuencia == ultima_actividad:
            lista.append(dato)
    return render_to_response('HtmlProyectoDesarrollo/lista_aprobacion_finalizacion.html',{'lista':lista,
                                                                               'id_proyecto':id_proyecto,
                                                                               'proyecto':proyecto})
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


