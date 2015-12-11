from mx.DateTime.DateTime import today
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from ProyectoDesarrollo.forms import UserStoryFormTiempo
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from Actividades.models import Actividad
from AdminProyectos.models import Proyecto
from UserStory.models import UserStory, US_Estado_ultimo, Historial_US,UserStory_aux,UserStory_Sprint
from django.contrib import messages
from Sprint.models import Sprint, Proyecto_En_Proceso
from django.core.mail import send_mail
from datetime import datetime, date, time, timedelta
import time
from Sprint.models import Estimacion_Proyecto, Estimacion_Sprint
import datetime
from django.template import RequestContext, loader
from django.http import HttpResponse
from Sprint.models import Sprint_En_Proceso,Dias_de_un_Sprint,Estimacion_Sprint
from django.core.exceptions import ObjectDoesNotExist
from PIC.models import RolUsuarioProyecto
import smtplib
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.db.models import F

@login_required(login_url='/admin/login/')
def kanban(request,id_proyecto):
    user=request.user
    rol=RolUsuarioProyecto.objects.get(usuario_id=user.id, proyecto_id=id_proyecto)
    actividades=Actividad.objects.filter(proyecto_id=id_proyecto).order_by("secuencia")
    userstorys=UserStory.objects.filter(proyecto_id=id_proyecto).order_by("prioridad")
    userstorys2=UserStory.objects.filter(proyecto_id=id_proyecto, estado='REASIGNAR_SPRINT').order_by("prioridad")
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
                                                                    'rol':rol,
                                                                    'userstorys':userstorys,'proyecto':proyecto,
                                                                    'sprints':sprints, 'id_proyecto':id_proyecto,
                                                                    'lista':lista})
def analizar_proyecto(id_proyecto):
    hoy=que_dia_es()
    print "hoy de proyecto"
    print hoy
    if hoy != 'Sabado' and hoy != 'Domingo':
        sprints=Sprint.objects.filter(proyecto_id=id_proyecto)
        us_sprint=UserStory_Sprint.objects.filter(proyecto_id=id_proyecto)
        ahora = date.today()
        print "ahora:"+str(ahora)
        try:
            proyecto_en_proceos=Proyecto_En_Proceso.objects.get(proyecto_id= id_proyecto,fecha=ahora)
        except ObjectDoesNotExist:
            proyecto_en_proceos=''
        horas_acumulada=0
        for s in us_sprint:
            horas_acumulada=horas_acumulada+s.horas_trabajadas
        print "hora acumulada del sprint:"+str(horas_acumulada)
        if proyecto_en_proceos != '':
            proyecto_en_proceos.horas_acumulada_sprint=horas_acumulada
            proyecto_en_proceos.save()
        if proyecto_en_proceos == '':
            proyecto_en_proceos=Proyecto_En_Proceso()
            proyecto_en_proceos.horas_acumulada_sprint=horas_acumulada
            proyecto_en_proceos.proyecto_id=id_proyecto
            proyecto_en_proceos.fecha=ahora
            proyecto_en_proceos.save()




def analizar_sprint(request, id_proyecto):
    """
    Se analiza el sprint en la fecha actual se guardan los datos de los user story del sprint hasta la fecha
    si hay mas de una consulta por dia solo se registra uno por dia
    :param request:
    :param id_proyecto:
    :return:
    """

    try:
        sprint=Sprint.objects.get(proyecto_id=id_proyecto ,estado='ABIERTO')
    except ObjectDoesNotExist:
        messages.debug(request, 'NO posee ningun sprint ABIERTO para su analisis')
        return HttpResponseRedirect('/proyecto/sprint/visualizar/'+str(id_proyecto))
    try:
        html_content = 'Prueba de conexion'
        send_mail('Prueba de conexion',html_content , 'gestorprojectpic@gmail.com', ['gestorprojectpic@gmail.com'], fail_silently=False)
    except smtplib.socket.gaierror:
        return HttpResponseRedirect('/error/conexion/')
    analizar_proyecto(id_proyecto)
    sprints=Sprint.objects.filter(proyecto_id=id_proyecto)
    sprint_fechas=Dias_de_un_Sprint.objects.filter(sprint_id=sprint.id).order_by('fecha')#tabla donde se guardan los dias de un sprint
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
    us_sprint=UserStory_Sprint.objects.filter(sprint_id=sprint.id)
    suma=0
    hoy=que_dia_es()
    ahora = date.today()

    for dato2 in us_sprint:
        suma+=dato2.horas_trabajadas
    for dato in sprint_fechas:
        bandera=True
        try:
            sprint_en_proceso=Sprint_En_Proceso.objects.get(sprint_id=sprint.id, fecha=fecha_actual_sprint)
        except ObjectDoesNotExist:
            bandera=False
        if fecha_actual_sprint == dato.fecha and hoy != 'Domingo' and hoy != 'Sabado' :
            if sprint.fechaInicio <= ahora and ahora <= sprint.fechaFin:
                print "ahora2"
                print ahora
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
            print 'hola123'
            sprint.estado='CERRADO'
            id_sprint=sprint.id
            siguiente=sprint.secuencia+1
            sprint.save()
            try:
                html_content = 'Su Proyecto   "'+proyecto.nombre+'"  a finalizado un Sprint Favor Fijarse si han terminados todos su user story"'
                send_mail('Finalizacion de Sprint',html_content , 'gestorprojectpic@gmail.com', [proyecto.scrumMaster.email], fail_silently=False)
            except smtplib.socket.gaierror:
                     return HttpResponseRedirect('/error/conexion/')
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
                        dato
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
                    try:
                        html_content = 'Su Proyecto   "'+proyecto.nombre+'"  a finalizado todos sus Sprint, pero quedan aun user storys sin concluir se creo un nuevo Sprint donde se han ubicado todos su user storys sin terminar  "'
                        send_mail('Finalizacion de todos sus Sprint-NO HAN TERMINADO SUS USER STORYS ',html_content , 'gestorprojectpic@gmail.com', [proyecto.scrumMaster.email], fail_silently=False)
                    except smtplib.socket.gaierror:
                        return HttpResponseRedirect('/error/conexion/')
                    proyecto.estado='REVISAR'
                    crear_nuevo_sprint(id_proyecto)

                if ban == 0:
                    try:
                        html_content = 'Su Proyecto   "'+proyecto.nombre+'"  a finalizado todos sus Sprint. Y sus user story estan todos Finalizados.   "'
                        send_mail('Finalizacion de todos sus Sprint',html_content , 'gestorprojectpic@gmail.com', [proyecto.scrumMaster.email], fail_silently=False)
                    except smtplib.socket.gaierror:
                        return HttpResponseRedirect('/error/conexion/')
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
    print 'mayortiempo'
    print mayor_tiempo
    if mayor_tiempo%8 == 0:
        valor=int(mayor_tiempo/8)
        print 'valor1'
        print valor
    else:
        valor=int(mayor_tiempo/8)
        valor+=1
    print 'valor2'
    print valor

    ultimo_sprint=0
    ahora = date.today()
    siguiente=0
    for dato in sprint:
        if ultimo_sprint < dato.secuencia:
            ultimo_sprint=dato.secuencia
    sprint2=Sprint.objects.get(proyecto_id=id_proyecto,secuencia=ultimo_sprint)
    fecha1=sprint2.fechaFin
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
    sprint_nuevo.tiempo_acumulado=(valor-1)*8
    sprint_nuevo.dia_trancurrido=0
    sprint_nuevo.dias_duracion=valor
    sprint_nuevo.suma_tiempo_usestory=0
    sprint_nuevo.save()
    sprint3=Sprint.objects.get(proyecto_id=id_proyecto,estado='ABIERTO')
    ######
    us_sprint=UserStory_Sprint()
    us_sprint.horas_trabajadas=0
    us_sprint.fecha=date.today()
    us_sprint.horas_estimada=0
    us_sprint.sprint_id=sprint3.id
    us_sprint.proyecto_id=id_proyecto
    us_sprint.save()
    ######
    suma=0
    for dato in userstory:
        ############################################################################################
        us_aux=UserStory()
        nombre=dato.nombre
        if nombre[-1] == ')' and nombre[-3] == '(' and nombre[-8] == 'e':
            nro=int(nombre[-2])
            us_aux.nombre=dato.nombre+'_extra('+str(nro+1)+')'
        else:
            us_aux.nombre=dato.nombre+'_extra(1)'
        ###///
        us_aux.sprint_id=sprint3.id
        us_aux.descripcion='UserStory extra de '+dato.nombre+'. '+dato.descripcion
        us_aux.fecha_creacion=today()
        us_aux.estado='TODO'
        us_aux.prioridad='ALTA'
        us_aux.tiempo_trabajado=0
        us_aux.tiempo_demas=0
        us_aux.tiempo_estimado=dato.tiempo_estimado-dato.tiempo_trabajado
        us_aux.actividad_id=dato.actividad.id
        us_aux.proyecto_id=id_proyecto
        us_aux.usuario_id=dato.usuario.id

        ###///
        historial_us=Historial_US()
        historial_us.nombre_us=dato.nombre
        historial_us.us_id=dato.id
        historial_us.fecha=today()
        historial_us.descripcion="Concluyo el Sprint del UserStory: "+dato.nombre+ "  , se le da como finalizado y se crea un User Story Extra: "+us_aux.nombre
        historial_us.proyecto_id=id_proyecto
        historial_us.save()
        ######
        historial_us=Historial_US()
        historial_us.nombre_us=us_aux.nombre
        historial_us.us_id=us_aux.id
        historial_us.fecha=today()
        historial_us.descripcion="Fue Creado el User Story extra:'"+us_aux.nombre+"' del User Story original:'"+dato.nombre+"'  y fue asignado al Sprint "+dato.sprint.nombre
        historial_us.proyecto_id=id_proyecto
        historial_us.save()
        #####
        us_aux.save()
        us_sprint=UserStory_Sprint.objects.get(sprint_id=sprint3.id)
        us_sprint.horas_estimada+=(dato.tiempo_estimado-dato.tiempo_trabajado)
        us_sprint.fecha=date.today()
        us_sprint.save()
        ######
        dato.estado='FINALIZADO'
        dato.save()

    ############################################################################################
    #######Dias del Sprint Nuevo#########33
    dias= valor
    contador=0
    while dias > contador:
        contador+=1
        dias_sprint=Dias_de_un_Sprint()
        fecha3=fecha_calcular(fecha1,contador-1)
        dias_sprint.dia=contador
        dias_sprint.fecha=fecha3
        dias_sprint.sprint_id=sprint3.id
        dias_sprint.save()
    ########MIRAR##################
    # estimacion_proyecto=Estimacion_Proyecto.objects.get(proyecto_id=id_proyecto)
    # estimacion_sprint=Estimacion_Sprint()
    # estimacion_sprint.proyecto_estimacion_id=estimacion_proyecto.id
    # estimacion_sprint.sprint_id=sprint3.id
    # estimacion_sprint.fechaInicio=sprint3.fechaInicio
    # estimacion_sprint.fechaFin=sprint3.fechaFin
    # estimacion_sprint.duracion=sprint3.tiempo_acumulado
    # estimacion_sprint.horas_hombre=suma
    # estimacion_sprint.save()

def visualizar_sprint_en_desarrollo(request,id_proyecto):
    proyecto=Proyecto.objects.get(pk=id_proyecto)
    ahora = date.today()
    user=request.user
    rol=RolUsuarioProyecto.objects.get(usuario_id=user.id, proyecto_id=id_proyecto)
    sprints=Sprint.objects.filter(proyecto_id=id_proyecto).order_by('secuencia')



    return render_to_response('HtmlProyectoDesarrollo/vizualizar_sprint.html',{'sprints':sprints,
                                                                               'id_proyecto':id_proyecto,
                                                                               'proyecto':proyecto,
                                                                               'rol':rol})

def observar_proceso_sprint(request, id_sprint):
    sprint=Sprint.objects.get(pk=id_sprint)
    sprint_estimado=Estimacion_Sprint.objects.get(sprint_id=id_sprint)
    tiempo_en_proceso=0
    ban=0
    hoy1=date.today()
    us2=UserStory.objects.filter(sprint_id=id_sprint)
    try:
        sprint_en_proceso=Sprint_En_Proceso.objects.filter(sprint_id=id_sprint).latest('fecha')
    except ObjectDoesNotExist:
        sprint_en_proceso=Sprint_En_Proceso()
        sprint_en_proceso.fecha=hoy1
        sprint_en_proceso.sprint_id=id_sprint
        sprint_en_proceso.horas_acumulada=0
        sprint_en_proceso.save()
    if sprint.estado == 'ABIERTO':
        mayor=0
        hoy = date.today()#fecha en anho-mes-dia
        hoy = str(hoy)
        rango_dia_inicio= "08:00:00"
        rango_dia_fin="12:00:00"
        rango_almuerzo_inicio="12:00:00"
        rango_almuerzo_fin="14:00:00"
        rango_tarde_inicio="14:00:00"
        rango_tarde_fin="18:00:00"
        ahora=time.strftime("%X")
        ahora=str(ahora)
        print ahora
        ahora_int = int(ahora[:2])
        try:
            dia_sprint=Dias_de_un_Sprint.objects.get(sprint_id=id_sprint, fecha=hoy)
        except ObjectDoesNotExist:
            dia_sprint=''
        if dia_sprint != '':
            dia=dia_sprint.dia
            print dia
            if rango_dia_inicio <= ahora and ahora <= rango_dia_fin:
                tiempo_en_proceso= (dia-1)*8+ahora_int-8
            else:
                if rango_tarde_inicio <= ahora and ahora <= rango_tarde_fin:
                    tiempo_en_proceso= (dia-1)*8+ahora_int-10
                else:
                    if rango_almuerzo_inicio <= ahora and ahora <= rango_almuerzo_fin:
                        tiempo_en_proceso= ((dia-1)*8)+4
                    else:
                        if rango_dia_inicio > ahora:
                            tiempo_en_proceso= (dia-1)*8
                        else:
                            tiempo_en_proceso= ((dia-1)*8)+8
    else:
        ban=1
    tiempo_hora_hombre_estimado=0
    tiempo_hora_hombre_proceso=0
    tiempo_hora_hombre_estimado=sprint_estimado.horas_hombre
    print "hola"
    print tiempo_en_proceso
    if ban == 1:
        tiempo_en_proceso=sprint_estimado.duracion
    return render_to_response('HtmlProyectoDesarrollo/observar_sprint.html',{'sprint':sprint,
                                                                               'sprint_estimado':sprint_estimado,
                                                                               'tiempo_en_proceso':tiempo_en_proceso,
                                                                               'tiempo_hora_hombre_estimado':tiempo_hora_hombre_estimado,
                                                                               'tiempo_hora_hombre_proceso':tiempo_hora_hombre_proceso,
                                                                               'sprint_en_proceso':sprint_en_proceso})




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
    user=request.user
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
        historial_us=Historial_US()
        historial_us.nombre_us=userstory.nombre
        historial_us.us_id=id_userstory
        historial_us.fecha=today()
        historial_us.descripcion="Fue Asignado a la Actividad "+userstory.actividad.nombre+ "  , por el usuario "+user.username
        historial_us.proyecto_id=id_proyecto
        historial_us.save()
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
    user=request.user
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
        if sprint.secuencia >= ultimo_sprint:
            us_aux=UserStory()
            nombre=userstory.nombre
            if nombre[-1] == ')' and nombre[-3] == '(' and nombre[-8] == 'e':
                nro=int(nombre[-2])
                us_aux.nombre=userstory.nombre+'_extra('+str(nro+1)+')'
            else:
                us_aux.nombre=userstory.nombre+'_extra(1)'
            ###///
            us_aux.sprint_id=sprint.id
            us_aux.descripcion='UserStory extra de '+userstory.nombre+'. '+userstory.descripcion
            us_aux.fecha_creacion=today()
            us_aux.estado='TODO'
            us_aux.prioridad='1'
            us_aux.tiempo_trabajado=0
            us_aux.tiempo_demas=0
            us_aux.tiempo_estimado=userstory.tiempo_estimado-userstory.tiempo_trabajado
            us_aux.actividad_id=userstory.actividad.id
            us_aux.proyecto_id=id_proyecto
            us_aux.usuario_id=userstory.usuario.id

            ###///
            userstory.estado=us_ultimo_estado.estado
            historial_us=Historial_US()
            historial_us.nombre_us=userstory.nombre
            historial_us.us_id=id_userstory
            historial_us.fecha=today()
            historial_us.descripcion="Concluyo el Sprint del UserStory: "+userstory.nombre+ "  , se le da como finalizado y se crea un User Story Extra: "+us_aux.nombre
            historial_us.proyecto_id=id_proyecto
            historial_us.save()
            ######
            historial_us=Historial_US()
            historial_us.nombre_us=us_aux.nombre
            historial_us.us_id=us_aux.id
            historial_us.fecha=today()
            historial_us.descripcion="Fue Creado el User Story extra:'"+us_aux.nombre+"' del User Story original:'"+userstory.nombre+"'  y fue asignado al Sprint "+userstory.sprint.nombre+ "  , por el usuario "+user.username
            historial_us.proyecto_id=id_proyecto
            historial_us.save()
            #####
            us_aux.save()
            us_sprint2=UserStory_Sprint.objects.filter(sprint_id=sprint.id).order_by('fecha')
            fecha_max='2015-01-01'
            for i in us_sprint2.reverse():
                if str(i.fecha) >= fecha_max:
                    us_sprint=i
            us_sprint.horas_estimada+=userstory.tiempo_estimado-userstory.tiempo_trabajado
            us_sprint.fecha=date.today()
            us_sprint.save()
            ######
            userstory.estado='FINALIZADO'
            userstory.save()
        if sprint.secuencia == ultimo_sprint:
            print "hola"
    if bandera == False:
        if sprint.secuencia > ultimo_sprint:
            print "hola2"

    messages.success(request, 'UserStory Reasignado al Sprint Siguiente')
    return HttpResponseRedirect('/userstory/lista/sprint/reasignar/'+str(id_proyecto))



def lista_reasignar_userstory_tiempo(request,id_proyecto):
    userstorys=UserStory.objects.filter(proyecto_id=id_proyecto,estado='REVISAR_TIEMPO')
    proyecto=Proyecto.objects.get(pk=id_proyecto)
    return render_to_response('HtmlProyectoDesarrollo/reasignar_userstory_tiempo.html',{'userstorys':userstorys,
                                                                               'id_proyecto':id_proyecto,
                                                                               'proyecto':proyecto})

def reasignar_userstory_tiempo(request,id_proyecto,id_userstory):
    userstory=UserStory.objects.get(pk=id_userstory)
    sprint=Sprint.objects.get(proyecto_id=id_proyecto, estado='ABIERTO')####
    id_sprint=sprint.id
    user=request.user
    if request.method=='POST':
        formulario= UserStoryFormTiempo(request.POST)
        if formulario.is_valid():
            formulario.clean()
            tiempo_estimado= formulario.cleaned_data['tiempo_estimado']
            print 'tiempo_estimado'
            print tiempo_estimado
            print 'tiempo del us'
            print userstory.tiempo_estimado
            if userstory.tiempo_estimado >= tiempo_estimado:
                messages.success(request,'Favor agregar un tiempo mayor de la que posee!!!!')
                return HttpResponseRedirect('/proyecto/us/tiempo/nuevo/'+str(id_proyecto)+'/'+str(id_proyecto))
            else:
                tiempo_estimado_anterior=0
                tiempo_estimado_anterior=userstory.tiempo_estimado
                userstory.tiempo_estimado= tiempo_estimado
                suma_de_tiempo_trabajado=0
                suma_de_tiempo_trabajado=userstory.tiempo_trabajado+userstory.tiempo_demas
                tiempo_demas=userstory.tiempo_demas
                print 'tiempo demas'
                print tiempo_demas
                userstory.tiempo_trabajado=suma_de_tiempo_trabajado
                userstory.tiempo_demas=0
                userstory.save()
                ######
                fecha_max='2015-01-01'
                us_sprint2=UserStory_Sprint.objects.filter(sprint_id=id_sprint)
                for i in us_sprint2.reverse():
                    if str(i.fecha) >= fecha_max:
                        us_sprint=i
                us_sprint.horas_estimada-=tiempo_estimado_anterior
                us_sprint.horas_estimada+=tiempo_estimado
                print 'us_sprint.horas_trabajadas'
                print us_sprint.horas_trabajadas
                #us_sprint.horas_trabajadas+=tiempo_demas
                us_sprint.save()
                ######
                completar_atributos_userstory_tiempo(id_userstory,id_sprint)
                historial_us=Historial_US()
                historial_us.nombre_us=userstory.nombre
                historial_us.us_id=id_userstory
                historial_us.fecha=today()
                historial_us.descripcion="Fue Asignado un nuevo tiempo "+str(userstory.tiempo_estimado)+ "  , por el usuario "+user.username
                historial_us.proyecto_id=id_proyecto
                historial_us.save()
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
    user=request.user
    rol=RolUsuarioProyecto.objects.get(usuario_id=user.id, proyecto_id=id_proyecto)
    proyecto=Proyecto.objects.get(pk=id_proyecto)
    sprints=Sprint.objects.filter(proyecto_id=id_proyecto).order_by('secuencia')
    return render_to_response('HtmlProyectoDesarrollo/burndowncharts.html',{'user':user,'proyecto':proyecto,
                                                                             'id_proyecto':id_proyecto,
                                                                             'sprints':sprints,
                                                                             'rol':rol},
                              context_instance=RequestContext(request))


def que_dia_es():
    x = datetime.datetime.now()

    dicdias = {'MONDAY':'Lunes','TUESDAY':'Martes','WEDNESDAY':'Miercoles','THURSDAY':'Jueves', \
    'FRIDAY':'Viernes','SATURDAY':'Sabado','SUNDAY':'Domingo'}
    anho = x.year
    mes =  x.month
    dia= x.day

    fecha = datetime.date(anho, mes, dia)
    dia = (dicdias[fecha.strftime('%A').upper()])
    print (dicdias[fecha.strftime('%A').upper()])
    return dia