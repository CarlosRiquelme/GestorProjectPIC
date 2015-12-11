# coding=UTF-8
from mx.DateTime.DateTime import today
from django.contrib.auth.models import User, Group, Permission
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from io import BytesIO
from reportlab.pdfgen import canvas
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from AdminProyectos.forms import ProyectoForm, ProyectoFormEdit
from AdminProyectos.models import Proyecto
from django.contrib import messages
from PIC.models import RolUsuarioProyecto
from mx.DateTime.DateTime import today
from datetime import datetime, date, time, timedelta
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from PIC.models import RolUsuarioProyecto
from Sprint.models import Sprint, Estimacion_Proyecto, Estimacion_Sprint
from UserStory.models import UserStory, UserStory_aux,UserStory_Sprint
from Actividades.models import Actividad
from Sprint.models import Dias_de_un_Sprint, Sprint_En_Proceso, Proyecto_En_Proceso
import smtplib
from django.core.exceptions import ObjectDoesNotExist


@login_required(login_url='/admin/login/')
def nuevo_proyecto(request):
    """
    Crea un nuevo proyecto
    """
    user=request.user
    #if not user.is_staff:
     #   return HttpResponseRedirect('/sinpermiso')
    bandera=True
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

                try:
                    html_content = 'Fue asignado a un Proyecto '+nombre+' ' \
                                                                    'Descripcion:'+descripcion+' ' \
                                                                                                   'Fecha Inicio:'+fecha.strftime('%Y/%m/%d')
                    send_mail('Asignado a Proyecto',html_content , 'gestorprojectpic@gmail.com', [email], fail_silently=False)
                except smtplib.socket.gaierror:
                     return HttpResponseRedirect('/error/conexion/')



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
    """
    Funcion que verifica si hay Proyectos que deben iniciar
    segun su fecha de inicio
    :param request:
    :return:
    """
    lista=[]
    ahora = date.today()
    proyectos=Proyecto.objects.all()
    for objeto in proyectos:
        try:
            actividad=Actividad.objects.get(proyecto_id=objeto.id,secuencia='1')
        except ObjectDoesNotExist:
            actividad=''
        try:
            sprint=Sprint.objects.get(proyecto_id=objeto.id,secuencia='1')
        except ObjectDoesNotExist:
            sprint=''
        userstory1=UserStory.objects.filter(proyecto_id=objeto.id)

        if actividad != '' and sprint != '' and  userstory1.exists():
            if objeto.fechaInicio <= ahora and objeto.estado == 'EN-ESPERA':
                scrum_master=objeto.scrumMaster
                fecha=objeto.fechaInicio
                try:
                    html_content = 'Su Proyecto "'+objeto.nombre+'"  a iniciado por llegar su fecha de Inicio  '+fecha.strftime('%Y/%m/%d')
                    send_mail('Asignado a Proyecto',html_content , 'gestorprojectpic@gmail.com', [scrum_master.email], fail_silently=False)
                except smtplib.socket.gaierror:
                    return HttpResponseRedirect('/error/conexion/')
                objeto.estado= 'EN-DESARROLLO'
                sprint=Sprint.objects.filter(proyecto_id=objeto.id).order_by("secuencia")
                fecha1=fecha
                estimacion_proyecto=Estimacion_Proyecto()
                estimacion_proyecto.fechaInicio=objeto.fechaInicio
                estimacion_proyecto.proyecto_id=objeto.id
                estimacion_proyecto.save()
                userstorys=UserStory.objects.filter(proyecto_id=objeto.id)
                ###################### Ya no se usa dejo por que no molesta #######################
                uno=1
                actividad=Actividad.objects.get(proyecto_id=objeto.id , secuencia=uno)
                actividades=Actividad.objects.filter(proyecto_id=objeto.id)
                cantidad_actividades=0
                peso_actividad=0.0
                for dato in actividades:
                    cantidad_actividades+=1
                peso_actividad=100/cantidad_actividades
                #############################################################################
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
                    contador=0
                    while dias > contador:
                        contador+=1
                        dias_sprint=Dias_de_un_Sprint()
                        fecha3=fecha_calcular(fecha1,contador-1)
                        dias_sprint.dia=contador
                        dias_sprint.fecha=fecha3
                        dias_sprint.sprint_id=dato.id
                        dias_sprint.save()
                    fecha2=fecha_calcular(fecha1,dias-1)
                    estimacion_sprint.fechaFin=fecha2
                    fecha1=fecha_calcular(fecha2,1)
                    sprint1.fechaFin=fecha2
                    sprint1.dias_duracion=dias
                    sprint1.dia_trancurrido=0
                    estimacion_sprint.duracion=dato.tiempo_acumulado
                    us=UserStory.objects.filter(sprint_id=dato.id)
                    suma=0
                    for i in us:
                        suma=suma+i.tiempo_estimado
                    estimacion_sprint.horas_hombre=suma
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
        ###########Carga los datos a la tabla aux del user story#########
        us_ax=UserStory_aux.objects.filter(proyecto_id=objeto.id)
        if not us_ax.exists():
            ###########################################################################
            #################Funcion donde se crea un aux a la tabla de US#############
            us=UserStory.objects.filter(proyecto_id=objeto.id).order_by('pk')
            for i in us:
                user_story2=UserStory_aux()
                user_story2.nombre=i.nombre
                user_story2.descripcion =i.descripcion
                user_story2.fecha_creacion=i.fecha_creacion
                user_story2.sprint_id=i.sprint_id
                user_story2.usuario_id=i.usuario_id
                user_story2.estado=i.estado
                user_story2.prioridad=i.prioridad
                user_story2.tiempo_trabajado=i.tiempo_trabajado
                user_story2.porcentaje=i.porcentaje
                user_story2.proyecto_id=i.proyecto_id
                user_story2.tiempo_estimado=i.tiempo_estimado
                user_story2.save()
            ############################################################################
        sprint=Sprint.objects.filter(proyecto_id=objeto.id)
        for i in sprint:
            suma_tiempo_estimado_us=0
            us=UserStory.objects.filter(proyecto_id=objeto.id, sprint_id=i.id)
            for j in us:
                suma_tiempo_estimado_us+=j.tiempo_estimado
            us_s=UserStory_Sprint()
            us_s.proyecto_id=objeto.id
            us_s.horas_estimada=suma_tiempo_estimado_us
            us_s.horas_trabajadas=0
            us_s.sprint_id=i.id
            us_s.fecha=ahora
            us_s.save()

    return render_to_response('HtmlProyecto/lista_proyectos_iniciados.html',{'lista':lista})
@login_required(login_url='/admin/login/')
def editar_proyecto(request, id_proyecto):
    """
    Edita un proyecto que aun no ha iniciado
    :param request:
    :param id_proyecto:
    :return:
    """
 
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
                {'formulario':formulario,'id_proyecto':id_proyecto,'user':user},
                              context_instance=RequestContext(request))
@login_required(login_url='/admin/login/')
def menu_proyecto(request):
    """
    Menu principal
    :param request:
    :return:
    """
    user=request.user
    return render_to_response('HtmlProyecto/menu_proyecto.html',{'user':user})

@login_required(login_url='/admin/login/')
def proyectos(request,id_user):
    """
    Lista todos los proyectos del Usuario
    :param request:
    :param id_user:
    :return:
    """
    usuarioproyecto=RolUsuarioProyecto.objects.filter(usuario_id=id_user)
    user=request.user
    proyectos=Proyecto.objects.filter(estado='ELIMINADO')

    return render_to_response('HtmlProyecto/proyectos.html',
                {'usuarioproyecto':usuarioproyecto,'user':user,
                 'proyectos':proyectos}, RequestContext(request))


@login_required(login_url='/admin/login/')
def eliminar_proyecto(request, id_proyecto):
    """
    Elimina un proyecto que aun no ha iniciado
    :param request:
    :param id_proyecto:
    :return:
    """

    proyecto= Proyecto.objects.get(pk=id_proyecto)
    user=request.user
    if proyecto.estado == 'ELIMINADO':
        nombre=proyecto.nombre
        proyecto.estado='EN-ESPERA'
        proyecto.save()
        messages.success(request,"Proyecto "+nombre+" Restaurado!")
        return HttpResponseRedirect('/proyectos/'+str(user.id))
    if proyecto.estado == 'EN-ESPERA':
        nombre=proyecto.nombre
        proyecto.estado='ELIMINADO'
        proyecto.save()
        messages.success(request,"Proyecto "+nombre+" Eliminado!")
        return HttpResponseRedirect('/proyectos/'+str(user.id))

def pre_eliminar_proyecto(request, id_proyecto):
    """
    Funcion de confirmacion de eliminacio del proyecto
    :param request:
    :param id_proyecto:
    :return:
    """
    user=request.user
    proyecto=Proyecto.objects.get(pk=id_proyecto)
    return render_to_response('HtmlProyecto/eliminarproyecto.html',{'proyecto':proyecto,
                                                                    'user':user},
                             context_instance=RequestContext(request))



@login_required(login_url='/admin/login/')
def mi_proyecto(request, id_proyecto):
    """
    Lista los atributos de un proyecto
    :param request:
    :param id_proyecto:
    :return:
    """
    proyecto= Proyecto.objects.get(pk=id_proyecto)
    user=request.user
    permiso=RolUsuarioProyecto.objects.get(usuario_id=user, proyecto_id=id_proyecto)


    return render_to_response('HtmlProyecto/miproyecto.html',
                                  {'proyecto':proyecto,
                                   'id_proyecto':id_proyecto,'user':user,
                                   'permiso':permiso},context_instance=RequestContext(request))


@login_required(login_url='/admin/login/')
def listar_usuario_proyecto(request, id_proyecto):
    """
    Lista los usuarios de un proyecto
    :param request:
    :param id_proyecto:
    :return:
    """
    usuarioproyecto=RolUsuarioProyecto.objects.filter(proyecto_id=id_proyecto).order_by('usuario')
    us=UserStory.objects.filter(proyecto_id=id_proyecto).exclude(usuario=None)

    proyecto=Proyecto.objects.get(pk=id_proyecto)
    paginator=Paginator(usuarioproyecto,5)
    page=request.GET.get('page')
    try:
        usuarioproyecto=paginator.page(page)
    except PageNotAnInteger:
        usuarioproyecto=paginator.page(1)
    except EmptyPage:
        usuarioproyecto=paginator.page(paginator.num_pages)

    return render_to_response('HtmlProyecto/lista_usuario_proyecto.html',{'usuarioproyecto':usuarioproyecto,
                                                                          'id_proyecto':id_proyecto, 'proyecto':proyecto},
                              context_instance=RequestContext(request))

@login_required(login_url='/admin/login/')
def asignar_usuario_proyecto(request, id_proyecto,id_user,id_rol):
    """
    Funcion que permite agregar un usuario a un proyecto
    :param request:
    :param id_proyecto:
    :param id_user:
    :param id_rol:
    :return:
    """
    usuarioproyecto=RolUsuarioProyecto()
    usuarioproyecto.proyecto_id=id_proyecto
    usuarioproyecto.usuario_id=id_user
    usuarioproyecto.rol_id=id_rol
    usuarioproyecto.save()
    messages.success(request, 'USUARIO ASIGNADO AL PROYECTO CORRECTAMENTE!')
    return HttpResponseRedirect('/proyecto/usuarios/'+str(id_proyecto))


@login_required(login_url='/admin/login/')
def listar_usuarios_para_asignar_proyecto(request, id_proyecto):
    """
    Lista los usuarios del sistema para agregarlos
    :param request:
    :param id_proyecto:
    :return:
    """
    lista=[]
    usuarioproyecto=RolUsuarioProyecto.objects.filter(proyecto_id=id_proyecto)
    usuarios=User.objects.all().order_by('username')
    usuario=request.user
    for user in usuarios:
        ban=1
        for user2 in usuarioproyecto:
            if user2.usuario.id == user.id: #si existe un usuario ya en tabla no quiero
                ban=0
        if ban == 1:
            lista.append(user)
    paginator=Paginator(lista,10)
    page=request.GET.get('page')
    try:
        lista=paginator.page(page)
    except PageNotAnInteger:
        lista=paginator.page(1)
    except EmptyPage:
        lista=paginator.page(paginator.num_pages)
    return render_to_response('HtmlProyecto/usuarios_asignar_proyecto.html',{'lista':lista,'usuarioproyecto':usuarioproyecto,
                                                                             'id_proyecto':id_proyecto,'user':usuario},
                              context_instance=RequestContext(request))


@login_required(login_url='/admin/login/')
def desasignar_usuario_proyecto(request, id_proyecto,id_user):
    """
    Desasignar a un usuario del proyecto
    :param request:
    :param id_proyecto:
    :param id_user:
    :return:
    """
    usuarioproyecto=RolUsuarioProyecto.objects.get(usuario_id=id_user, proyecto_id=id_proyecto)
    usuarioproyecto.delete()
    messages.success(request, 'USUARIO DESASIGNADO AL PROYECTO CORRECTAMENTE!')
    return HttpResponseRedirect('/proyecto/usuarios/'+str(id_proyecto))


@login_required(login_url='/admin/login/')
def listar_roles_para_asignar_usuario(request, id_proyecto):
    """
    Lista los distintos roles para el proyecto
    :param request:
    :param id_proyecto:
    :return:
    """
    roles=Group.objects.all()
    usuarioproyecto=RolUsuarioProyecto.objects.filter(proyecto_id=id_proyecto)

    return render_to_response('HtmlProyecto/usuarios_asignar_proyecto.html',{'roles':roles,'usuarioproyecto':usuarioproyecto,
                                                                             'id_proyecto':id_proyecto},
                              context_instance=RequestContext(request))

(MON, TUE, WED, THU, FRI, SAT, SUN) = range(7)

def fecha_calcular(start, days, holidays=(), workdays=(MON,TUE,WED,THU,FRI)):
    """
    Calcula la fecha sin tener en cuenta los dias domingos y sabados
    :param start:
    :param days:
    :param holidays:
    :param workdays:
    :return:
    """
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

@login_required(login_url='/admin/login/')
def scrum_master_vista(request, id_proyecto):
    """
    Vista de Administracion del ScrumMaster del Proyecto donde crea/modidifica/elimina/verifica/aprueba/habilita
    user story , sprint, usuarios,
    :param request:
    :param id_proyecto:
    :return:
    """
    user=request.user
    proyecto=Proyecto.objects.get(pk=id_proyecto)
    return render_to_response('HtmlProyecto/scrumMaster.html',{'user':user,'proyecto':proyecto,
                                                                             'id_proyecto':id_proyecto},
                              context_instance=RequestContext(request))
@login_required(login_url='/admin/login/')
def finalizar_proyecto(request, id_proyecto):
    userstorys=UserStory.objects.filter(proyecto_id=id_proyecto)
    sprints=Sprint.objects.filter(proyecto_id=id_proyecto)
    proyecto=Proyecto.objects.get(pk=id_proyecto)
    ban='TRUE'
    ban2='TRUE'
    lista_userstory=[]
    lista_sprints=[]
    for dato in userstorys:
        if dato.estado != 'FINALIZADO' and dato.estado != 'CANCELADO':
            ban='FALSE'
            lista_userstory.append(dato)
    for dato in sprints:
        if dato.estado != 'CERRADO':
            ban2='FALSE'
            lista_sprints.append(dato)

    if ban == 'TRUE' and ban2 == 'TRUE':
        proyecto.estado='FINALIZADO'
        ahora = date.today()
        try:
            html_content = 'EL PROYECTO A FINALIZADO'+proyecto.nombre+' ' 'Descripcion:'+proyecto.descripcion+' ''Fecha de Finalizacion :'+str(ahora)
            send_mail('Finalizacion del Proyecto',html_content , 'gestorprojectpic@gmail.com', [proyecto.scrumMaster.email], fail_silently=False)
        except smtplib.socket.gaierror:
             return HttpResponseRedirect('/error/conexion/')
        proyecto.save()
        messages.success(request, 'A FINALIZADO CORRECTAMENTE EL PROYECTO!')
        return HttpResponseRedirect('/proyecto/scrumMaster/'+str(id_proyecto))

    else:
        return render_to_response('HtmlProyecto/lista_sprint_us_sin_finalizar.html',{'proyecto':proyecto,
                                                               'id_proyecto':id_proyecto,
                                                               'sprints':lista_sprints,
                                                               'userstorys':lista_userstory,
                                                               'ban':ban,
                                                               'ban2':ban2},
                              context_instance=RequestContext(request))

@login_required(login_url='/admin/login/')
def lista_sprint_para_graficar(request,id_proyecto):
    """
    Lista todos los sprint para que puedan ser graficados por la funcion jo5
    :param request:
    :param id_proyecto:
    :return:
    """
    proyecto=Proyecto.objects.get(pk=id_proyecto)
    sprints=Sprint.objects.filter(proyecto_id=id_proyecto)
    return render_to_response('HtmlProyecto/lista_sprints_para_graficar.html',{'proyecto':proyecto,
                                                               'id_proyecto':id_proyecto,
                                                               'sprints':sprints},
                              context_instance=RequestContext(request))


def jo5(request,id_sprint):
    """
    Funcion que grafica un sprint en particular
    :param request:
    :param id_sprint:
    :return:
    """

    userstorys = UserStory_aux.objects.filter(sprint_id = id_sprint)
    sprint = Sprint.objects.get(pk=id_sprint)
    # try:
    #     sprint_proceso=Sprint_En_Proceso.objects.get(sprint_id=id_sprint)
    # except ObjectDoesNotExist:
    #     sprint_proceso=''
    # cantidad=0
    # if sprint_proceso != '':
    #     for aux in sprint_proceso:
    #         cantidad+=1

    v = []
    v2 = []

    suma = 0
    for aux1 in userstorys:
        suma = suma + aux1.tiempo_estimado



    c=0
    # contador=0
    # for au in userstorys:
    #     if cantidad !=0 and contador < cantidad:
    #         contador+=1
    #         aeiou = au.suma_trabajadas
    #         v3.append(v3[c]-aeiou)
    #         c=c+1


    v.append(suma)
    v2.append('Al Inicio')

    aux2 = 1
    for d in userstorys:
        if(aux2 <= d.tiempo_estimado):
            aux2 = d.tiempo_estimado



    dias1 = float(aux2)/8.0

    dias2 = float(aux2)//8.0



    if (dias1>dias2):
        dias1 = dias1 + 1.0

    dias1 = int(dias1)


    uss = []
    c = 0
    for op in userstorys:
        uss.append(op)
        #print(op.tiempo_estimado)
        #print(uss[c].tiempo_estimado)
        c = c + 1


    c = 0
    for i in range(0, dias1):
        tie = 0
        for d in uss:
            #print(d.tiempo_estimado)
            if (d.tiempo_estimado < 8):
                tie = tie + d.tiempo_estimado
                d.tiempo_estimado = 0
            else:
                tie = tie + 8
                d.tiempo_estimado = d.tiempo_estimado - 8


        aux = v[c]
        v.append( aux - tie)
        c = c + 1
        #v2.append(str(c))

    c = 0
    sprint_por_dia = Dias_de_un_Sprint.objects.filter(sprint_id = id_sprint)
    for i in range(0, dias1):
        print (i)
        for j in sprint_por_dia:
            if(j.dia==(i+1)):
                v2.append(str(j.fecha))





    #v2.append(fec)
    lista108 = v
    lista300 = v2

###divague

    userstorys = UserStory_aux.objects.filter(sprint_id = id_sprint)
    sprint = Sprint.objects.get(pk=id_sprint)
    cantidad=0
    cantidad=Sprint_En_Proceso.objects.filter(sprint_id=id_sprint).count()
    sprint_proceso=Sprint_En_Proceso.objects.filter(sprint_id=id_sprint).order_by('pk')
    print "cantidad: "+str(cantidad)
    v = [] #eje y estimado
    v2 = [] # eje x
    v3 = [] # eje y en proceso
    #####################CALCULO DE ESTIMACION DEL SPRINT#######################
    suma = 0
    for aux1 in userstorys:
        suma = suma + aux1.tiempo_estimado

    v.append(suma)
    v2.append('Al Inicio')
    userstorys_actual=UserStory.objects.filter(sprint_id=id_sprint)
    suma_actual = 0
    for aux1 in userstorys_actual:
        suma_actual = suma_actual + aux1.tiempo_estimado
    ##################### FIN=======CALCULO DE ESTIMACION DEL SPRINT#######################
    v3.append(suma_actual)

    c=0
    contador=0


    #############Calculo del Sprint en proceso#######################
    us_sprint=UserStory_Sprint.objects.filter(sprint_id=id_sprint)

    for i in us_sprint:
        suma_estimadas_del_sprint=0
        suma_trabajadas_del_sprint=0
        suma_estimadas_del_sprint=suma_estimadas_del_sprint+i.horas_estimada
        suma_trabajadas_del_sprint+=i.horas_trabajadas
        resta=0
        resta=suma_estimadas_del_sprint-suma_trabajadas_del_sprint
        #v2.append(str(i.fecha))
        v3.append(resta)
    #########################################3




    #v2.append(fec)
    lista1 = v
    lista3 = v2
    #lista3 = [0,1,2,3,4,5]
    #lista3 = pipo
    #lista3.append(fec)
    lista2 = v3
    print "lista1 o v"
    print v
    print "lista3 o v2"
    print v2
    print "lista2 o v3"
    print v3

    """
        ----------------------------- OBSERVACION-----------------------------
        La lista v tiene los datos del sprint de lo que tiene que hace
        por dia
        La lista V2 los dias o las fechas
        esto hay que guardar en la base de datos con el id del sprint
        ----------------------------------------------------------------------
    """

    return render_to_response('line-basic3/index.html',{'lista3':lista300,'lista2':lista108,'lista1':lista2})
def jo3(request,id_proyecto):
    """
    Funcion que grafica la estimacion del proyecto con lo que se esta desarrollando
    :param request:
    :param id_proyecto:
    :return:
    """
    userstorys=UserStory_aux.objects.filter(proyecto_id=id_proyecto)


    lista1=[]   #Lista donde se guarda las estimacion del proyecto
    lista3=[]   #Lista de las fechas del proyecto
    lista4=[]   #Lista donde esta los datos del proceso de desarrollo del Proyecto
    suma_estimacion_us = 0


    aux23 = 0
    for dato in userstorys:
        suma_estimacion_us = suma_estimacion_us  + dato.tiempo_estimado
        aux23 = suma_estimacion_us
        aux_suma_estimacion_us=suma_estimacion_us

    lista4.append(suma_estimacion_us)
    lista1.append(suma_estimacion_us)
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    op = str(proyecto.fechaInicio)
    lista3.append(op)


    ######################ESTIMACION DEL PROYECTO####################333
    sprints = Sprint.objects.filter(proyecto_id=id_proyecto).order_by("fechaInicio")
    us_aux=UserStory_aux.objects.filter(proyecto_id=id_proyecto).order_by("sprint_id")
    for dato1 in sprints:
        suma = 0
        for dato2 in us_aux:
            if(dato2.sprint_id == dato1.id):
                suma = suma + dato2.tiempo_estimado
        suma_estimacion_us = suma_estimacion_us - suma
        lista1.append(suma_estimacion_us)
        lista3.append(str(dato1.fechaFin))
    #########################FIN DE ESTIMACION DEL PROYECTO####################
    print "sprint"
    print sprints
    proyecto_en_proceso=Proyecto_En_Proceso.objects.filter(proyecto_id=id_proyecto).order_by("fecha")

# resta=0
# fecha_max='2015-01-01'
# if proyecto_en_proceso.exists():
#     for sp in sprints:
#         for pep in proyecto_en_proceso.reverse():
#             if sp.fechaInicio <= pep.fecha and pep.fecha <= sp.fechaFin:
#                 if fecha_max < str(pep.fecha):
#                     fecha_max=str(pep.fecha)
#                     resta=aux_suma_estimacion_us-pep.horas_acumulada_sprint
#                     lista4.append(resta)
# else:
#     lista4.append(aux_suma_estimacion_us)
    ##########################CALCULO DE SPRINT EN PROCESO######################333
    suma_horas_sprint_trabajado=0
    for s in sprints:

        suma_horas_sprint_estimado=0
        us_del_sprint=UserStory.objects.filter(sprint_id=s.id)
        if s.estado == 'ABIERTO' or s.estado == 'CERRADO':
            for us in us_del_sprint:
                suma_horas_sprint_trabajado+=us.tiempo_trabajado
                suma_horas_sprint_estimado+=us.tiempo_estimado
            resta=0
            resta=aux23-suma_horas_sprint_trabajado
            lista4.append(resta)


    ##########################FIN DEL CALCULO DEL SPRINT DEL PROCESO###############
    #lista1 = [120, 100,90,80,70,60,50,40,30,20,10,0]
    lista2 = lista4
    #lista3 = ['1', ' 2', ' 3', ' 4', ' 5', ' 6',
    #            ' 7', ' 8', ' 9', ' 10', ' 11', ' 12']
    return render_to_response('line-basic2/index.html',{'lista3':lista3,'lista2':lista1,'lista1':lista2})

#################################################################################################
#############################     A PARTIR DE ACA LOS               #############################
#############################     DISTITNTOS REPORTES               #############################
#################################################################################################
def graficadeultimosprint(request,id_sprint):

    return render_to_response('line-basic2/index.html',{'lista3':lista3,'lista2':lista1,'lista1':lista2})


def reporte01(request,id_proyecto):
    id_proyecto = id_proyecto
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = '; filename="reporte01.pdf"'

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.

    proyecto=Proyecto.objects.get(pk=id_proyecto)
    userstorys=UserStory.objects.filter(proyecto_id=id_proyecto)
    pu = RolUsuarioProyecto.objects.filter(proyecto_id=id_proyecto).order_by('rol')
    user = User.objects.all()

    palabra2 = "GestorProjectPIC"
    palabra = "Cantidad de Trabajo en Curso por el Equipo"
    palabra3 = "Proyecto : " + proyecto.nombre
    palabra4 = "Estado : " + proyecto.estado
    palabra5 = "Scrum Master: " + str(proyecto.scrumMaster).capitalize()
    palabra6 = "Equipo:"



    p.setFontSize(size=14, leading=None)
    p.drawString(150, 800, palabra)
    p.setFontSize(size=8, leading=None)
    p.drawString(250, 790, palabra2)

    palabra13="_________________________________________________________________________"
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 775, palabra13)

    p.setFontSize(size=12, leading=None)
    p.drawString(45, 760, palabra3)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 740, palabra4)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 720, palabra5)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 700, palabra6)

    c=15
    a=700
    vect = []
    for b in pu:
        if b.rol.name == 'Equipo':
            palabra7 = "             - " +str(b.usuario).capitalize()
            p.setFontSize(size=12, leading=None)
            a=a-c
            p.drawString(45, a, palabra7)
        if b.rol.name == 'Cliente':
            a=a-c
            palabra13 = "Cliente:"
            p.setFontSize(size=12, leading=None)
            p.drawString(45, a, palabra13)
            a=a-c
            palabra13 = "             - " +str(b.usuario).capitalize()
            p.drawString(45, a, palabra13)
    a=a-10
    palabra13="_________________________________________________________________________"
    p.setFontSize(size=12, leading=None)
    p.drawString(45, a , palabra13)

    a=a-30
    palabra8 = "User Storys:"
    p.setFontSize(size=12, leading=None)
    p.drawString(45, a, palabra8)

    ussss = UserStory.objects.filter(proyecto_id=id_proyecto).order_by('fecha_creacion')
    c=0
    d=0
    for cont in ussss:
        palabra9 =  "-Nombre :   " + str(cont.nombre).capitalize()
        palabra10 = "-Usuario Responsable    :    "+ (cont.usuario.username).capitalize()
        palabra11 = "*Tiempo Estimado:       " + str(cont.tiempo_estimado)
        palabra12 = "*Tiempo Trabajado:      " + str(cont.tiempo_trabajado)
        a = a - 20
        b = a - 15
        c = b - 15
        d = c - 15
        p.setFontSize(size=11, leading=None)
        p.drawString(100, a, palabra9)
        p.setFontSize(size=11, leading=None)
        p.drawString(100, b, palabra10)
        p.setFontSize(size=11, leading=None)
        p.drawString(150, c, palabra11)
        p.setFontSize(size=11, leading=None)
        p.drawString(150, d, palabra12)
        a = d

    p.showPage()
    p.save()
    return response

def lista_de_reportes(request,id_proyecto):
    lista3 = id_proyecto
    return render_to_response('HtmlReportes/ReportePrincipal.html',{'lista3':lista3})



def reporte02(request,id_proyecto):
    # Create the HttpResponse object with the appropriate PDF headers.

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = '; filename="reporte02.pdf"'

    buffer = BytesIO()


    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    TPendientes = UserStory.objects.filter(proyecto_id=id_proyecto).filter(estado="CREADO")
    TFinalizados = UserStory.objects.filter(proyecto_id=id_proyecto).filter(estado="FINALIZADO")
    TenCursos = UserStory.objects.filter(proyecto_id=id_proyecto).exclude(estado="CREADO").exclude(estado="FINALIZADO").exclude(estado="CANCELADO")
    proyecto=Proyecto.objects.get(pk=id_proyecto)
    userstorys=UserStory.objects.filter(proyecto_id=id_proyecto)
    UsuariosProyectos = RolUsuarioProyecto.objects.filter(proyecto_id=id_proyecto).order_by('rol')
    for jo in UsuariosProyectos:
        user = User.objects.filter(id=jo.usuario_id)

    palabra2 = "GestorProjectPIC"
    palabra = "Cantidad de Trabajo por Usuario Pendiente, en Curso y Finalizados."
    palabra3 = "Proyecto : " + proyecto.nombre.capitalize()
    palabra4 = "Estado : " + proyecto.estado
    palabra5 = "Scrum Master: " + str(proyecto.scrumMaster).capitalize()
    palabra6 = "Equipo:"



    p.setFontSize(size=14, leading=None)
    p.drawString(100, 800, palabra)
    p.setFontSize(size=8, leading=None)
    p.drawString(270, 790, palabra2)

    palabra13="_________________________________________________________________________"
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 775, palabra13)

    p.setFontSize(size=12, leading=None)
    p.drawString(45, 760, palabra3)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 740, palabra4)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 720, palabra5)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 700, palabra6)
    c=15
    a=700
    for b in UsuariosProyectos:
        if b.rol.name == 'Equipo':
            palabra7 = "             - " +str(b.usuario).capitalize()
            p.setFontSize(size=12, leading=None)
            a=a-c
            p.drawString(45, a, palabra7)
        if b.rol.name == 'Cliente':
            a=a-c
            palabra13 = "Cliente:"
            p.setFontSize(size=12, leading=None)
            p.drawString(45, a, palabra13)
            a=a-c
            palabra13 = "             - " +str(b.usuario).capitalize()
            p.drawString(45, a, palabra13)
    palabra13="_________________________________________________________________________"
    salto = a-10
    p.setFontSize(size=12, leading=None)
    p.drawString(45, salto, palabra13)
    for a in UsuariosProyectos:
        if a.rol.name == 'Equipo':
            userstorys2=UserStory.objects.filter(proyecto_id=id_proyecto,usuario_id=a.usuario_id)
            palabra9 = str(a.usuario).capitalize()+":"
            salto = salto - 15
            p.setFontSize(size=11, leading=None)
            p.drawString(45, salto, palabra9)
            palabra10 = "Trabajos Pendientes:  "
            salto = salto - 15
            p.setFontSize(size=9, leading=None)
            p.drawString(100, salto, palabra10)
            print "holaaaa"
            for i in userstorys2:
                if i.estado == 'CREADO':
                    palabra11 = "                  -" + str(i.nombre).capitalize()
                    salto = salto - 15
                    p.setFontSize(size=9, leading=None)
                    p.drawString(150, salto, palabra11)
            palabra14 = "Trabajos En Cursos:  "
            salto = salto - 15
            p.setFontSize(size=9, leading=None)
            p.drawString(100, salto, palabra14)
            for i in userstorys2:
                if i.estado != 'CREADO' and i.estado != 'FINALIZADO' and i.estado != 'CANCELADO':
                    palabra11 = "                  -" + str(i.nombre).capitalize()
                    salto = salto - 15
                    p.setFontSize(size=9, leading=None)
                    p.drawString(150, salto, palabra11)
            palabra12 = "Trabajos Finalizados:  "
            salto = salto - 15
            p.setFontSize(size=9, leading=None)
            p.drawString(100, salto, palabra12)
            for i in userstorys2:
                if  i.estado == 'FINALIZADO':
                    palabra11 = "                  -" + str(i.nombre).capitalize()
                    salto = salto - 15
                    p.setFontSize(size=9, leading=None)
                    p.drawString(150, salto, palabra11)
    # Close the PDF object cleanly.
    p.showPage()
    p.save()
    return response

def reporte03(request,id_proyecto):
    id_proyecto = id_proyecto
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = '; filename="reporte03.pdf"'

    buffer = BytesIO()

    p = canvas.Canvas(response)

    proyecto=Proyecto.objects.get(pk=id_proyecto)
    userstorys=UserStory.objects.filter(proyecto_id=id_proyecto)
    UsuariosProyectos = RolUsuarioProyecto.objects.filter(proyecto_id=id_proyecto).order_by('rol')
    user = User.objects.all()

    palabra2 = "GestorProjectPIC"
    palabra = "Lista clasificada por orden de prioridad de todas las actividades para completar el proyecto."
    palabra3 = "Proyecto : " + proyecto.nombre.capitalize()
    palabra4 = "Estado : " + proyecto.estado
    palabra5 = "Scrum Master: " + str(proyecto.scrumMaster).capitalize()
    palabra6 = "Equipo:"




    p.setFontSize(size=12, leading=None)
    p.drawString(55, 800, palabra)
    p.setFontSize(size=8, leading=None)
    p.drawString(270, 790, palabra2)

    palabra13="_________________________________________________________________________"
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 775, palabra13)

    p.setFontSize(size=12, leading=None)
    p.drawString(45, 760, palabra3)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 740, palabra4)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 720, palabra5)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 700, palabra6)
    c=15
    a=700
    for b in UsuariosProyectos:
        if b.rol.name == 'Equipo':
            palabra7 = "             - " +str(b.usuario).capitalize()
            p.setFontSize(size=12, leading=None)
            a=a-c
            p.drawString(45, a, palabra7)
        if b.rol.name == 'Cliente':
            a=a-c
            palabra13 = "Cliente:"
            p.setFontSize(size=12, leading=None)
            p.drawString(45, a, palabra13)
            a=a-c
            palabra13 = "             - " +str(b.usuario).capitalize()
            p.drawString(45, a, palabra13)
    palabra13="_________________________________________________________________________"
    salto = a-10
    p.setFontSize(size=12, leading=None)
    p.drawString(45, salto, palabra13)
    salto=salto-20
    palabra8 = "Actividades:"
    p.setFontSize(size=14, leading=None)
    p.drawString(45, salto, palabra8)
    salto = salto-15

    actividades=Actividad.objects.filter(proyecto_id=id_proyecto)

    c=0
    for i in actividades:
        c=c+1
        palabra9 = "-Nombre: " + str(i.nombre).capitalize()
        palabra10 = "-Prioridad: " + str(i.secuencia)
        p.setFontSize(size=12, leading=None)
        p.drawString(150, salto, palabra9)
        salto = salto -15
        p.setFontSize(size=12, leading=None)
        p.drawString(150, salto, palabra10)
        salto = salto -25

    p.showPage()
    p.save()
    return response

def reporte04(request,id_proyecto):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = '; filename="reporte04.pdf"'

    buffer = BytesIO()

    p = canvas.Canvas(response)


    proyecto=Proyecto.objects.get(pk=id_proyecto)
    sprints=Sprint.objects.filter(proyecto_id=id_proyecto)
    userstorys=UserStory.objects.filter(proyecto_id=id_proyecto)
    UsuariosProyectos = RolUsuarioProyecto.objects.filter(proyecto_id=id_proyecto).order_by('rol')
    user = User.objects.all()

    palabra2 = "GestorProjectPIC"
    palabra = "Lista de Tiempo estimado"
    palabra3 = "Proyecto : " + proyecto.nombre
    palabra4 = "Estado : " + proyecto.estado
    palabra5 = "Scrum Master: " + str(proyecto.scrumMaster).capitalize()
    palabra6 = "Equipo:"


    p.setFontSize(size=14, leading=None)
    p.drawString(225, 800, palabra)
    p.setFontSize(size=8, leading=None)
    p.drawString(270, 790, palabra2)

    palabra13="_________________________________________________________________________"
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 775, palabra13)

    p.setFontSize(size=12, leading=None)
    p.drawString(45, 760, palabra3)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 740, palabra4)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 720, palabra5)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 700, palabra6)
    c=15
    a=700
    for b in UsuariosProyectos:
        if b.rol.name == 'Equipo':
            palabra7 = "             - " +str(b.usuario).capitalize()
            p.setFontSize(size=12, leading=None)
            a=a-c
            p.drawString(45, a, palabra7)
        if b.rol.name == 'Cliente':
            a=a-c
            palabra13 = "Cliente:"
            p.setFontSize(size=12, leading=None)
            p.drawString(45, a, palabra13)
            a=a-c
            palabra13 = "             - " +str(b.usuario).capitalize()
            p.drawString(45, a, palabra13)
    palabra13="_________________________________________________________________________"
    salto = a-10
    p.setFontSize(size=12, leading=None)
    p.drawString(45, salto, palabra13)
    salto=salto-20

    palabra8 = "Lista de tiempo estimado"
    p.setFontSize(size=14, leading=None)
    p.drawString(45, 600, palabra8)
    salta = 600

    palabra9 = "-Proyecto: " + str(proyecto.nombre)
    palabra10 = "--Fecha de Inicio: " + str(proyecto.fechaInicio)
    palabra11 = "--Fecha de Finalizacion " + str(proyecto.fechaFin)
    salta = salta-20
    p.setFontSize(size=12, leading=None)
    p.drawString(100, salta, palabra9)

    salta = salta-15
    p.setFontSize(size=12, leading=None)
    p.drawString(130, salta, palabra10)

    salta = salta-15
    p.setFontSize(size=12, leading=None)
    p.drawString(130, salta, palabra11)


    palabra12 = "-Sprints"
    salta = salta-30
    p.setFontSize(size=12, leading=None)
    p.drawString(100, salta, palabra12)

    for i in sprints:
        palabra13 = "--Nombre: " + str(i.nombre)
        salta = salta - 25
        p.setFontSize(size=12, leading=None)
        p.drawString(130, salta, palabra13)
        palabra14 = "*Fecha Inicio: " + str(i.fechaInicio)
        salta = salta-15
        p.setFontSize(size=12, leading=None)
        p.drawString(150, salta, palabra14)
        palabra15 = "*Fecha Inicio: " + str(i.fechaFin)
        salta = salta-15
        p.setFontSize(size=12, leading=None)
        p.drawString(150, salta, palabra15)

    p.showPage()
    p.save()
    return response
def reporte05(request,id_proyecto):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = '; filename="reporte05.pdf"'

    buffer = BytesIO()

    p = canvas.Canvas(response)


    proyecto=Proyecto.objects.get(pk=id_proyecto)
    userstorys=UserStory.objects.filter(proyecto_id=id_proyecto)
    UsuariosProyectos = RolUsuarioProyecto.objects.filter(proyecto_id=id_proyecto).order_by('rol')
    user = User.objects.all()

    palabra2 = "GestorProjectPIC"
    palabra = "Backlog de Producto"
    palabra3 = "Proyecto : " + proyecto.nombre
    palabra4 = "Estado : " + proyecto.estado
    palabra5 = "Scrum Master: " + str(proyecto.scrumMaster).capitalize()
    palabra6 = "Equipo:"

    p.setFontSize(size=14, leading=None)
    p.drawString(225, 800, palabra)
    p.setFontSize(size=8, leading=None)
    p.drawString(260, 790, palabra2)

    palabra13="_________________________________________________________________________"
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 775, palabra13)

    p.setFontSize(size=12, leading=None)
    p.drawString(45, 760, palabra3)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 740, palabra4)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 720, palabra5)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 700, palabra6)

    c=15
    a=700
    for b in UsuariosProyectos:
        if b.rol.name == 'Equipo':
            palabra7 = "             - " +str(b.usuario).capitalize()
            p.setFontSize(size=12, leading=None)
            a=a-c
            p.drawString(45, a, palabra7)
        if b.rol.name == 'Cliente':
            a=a-c
            palabra13 = "Cliente:"
            p.setFontSize(size=12, leading=None)
            p.drawString(45, a, palabra13)
            a=a-c
            palabra13 = "             - " +str(b.usuario).capitalize()
            p.drawString(45, a, palabra13)
    palabra13="_________________________________________________________________________"
    salto = a-10
    p.setFontSize(size=12, leading=None)
    p.drawString(45, salto, palabra13)
    salto=salto-20


    palabra8 = "User Storys"
    p.setFontSize(size=12, leading=None)
    p.drawString(45, salto, palabra8)


    a = salto

    sprints = Sprint.objects.filter(proyecto_id=id_proyecto).order_by('secuencia')
    for i in sprints:
        print i.secuencia
        ussss = UserStory_aux.objects.filter(proyecto_id=id_proyecto,sprint_id=i.id).order_by('prioridad')
        c=0
        for cont in ussss:
            palabra9 = "-Nombre: " + str(cont.nombre)
            palabra10 = "*Tiempo Estimado: " + str(cont.tiempo_estimado)

            a = a - 15
            b = a - 15
            c = b - 15
            p.setFontSize(size=12, leading=None)
            p.drawString(100, a, palabra9)
            p.setFontSize(size=12, leading=None)
            p.drawString(130, b, palabra10)
            a = c

    p.showPage()
    p.save()
    return response

def reporte06(request,id_proyecto):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = '; filename="reporte06.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(response)

    proyecto=Proyecto.objects.get(pk=id_proyecto)
    userstorys=UserStory.objects.filter(proyecto_id=id_proyecto)
    sprints = Sprint.objects.filter(proyecto_id=id_proyecto)
    UsuariosProyectos = RolUsuarioProyecto.objects.filter(proyecto_id=id_proyecto).order_by('rol')
    user = User.objects.all()

    palabra2 = "GestorProjectPIC"
    palabra = "Backlog de Sprints"
    palabra3 = "Proyecto : " + proyecto.nombre
    palabra4 = "Estado : " + proyecto.estado
    palabra5 = "Scrum Master: " + str(proyecto.scrumMaster).capitalize()
    palabra6 = "Equipo:"

    p.setFontSize(size=14, leading=None)
    p.drawString(225, 800, palabra)
    p.setFontSize(size=8, leading=None)
    p.drawString(260, 790, palabra2)

    palabra13="_________________________________________________________________________"
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 775, palabra13)

    p.setFontSize(size=12, leading=None)
    p.drawString(45, 760, palabra3)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 740, palabra4)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 720, palabra5)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 700, palabra6)

    c=15
    a=700
    for b in UsuariosProyectos:
        if b.rol.name == 'Equipo':
            palabra7 = "             - " +str(b.usuario).capitalize()
            p.setFontSize(size=12, leading=None)
            a=a-c
            p.drawString(45, a, palabra7)
        if b.rol.name == 'Cliente':
            a=a-c
            palabra13 = "Cliente:"
            p.setFontSize(size=12, leading=None)
            p.drawString(45, a, palabra13)
            a=a-c
            palabra13 = "             - " +str(b.usuario).capitalize()
            p.drawString(45, a, palabra13)
    palabra13="_________________________________________________________________________"
    salto = a-10
    p.setFontSize(size=12, leading=None)
    p.drawString(45, salto, palabra13)
    salto=salto-20


    palabra8 = "Sprints y sus UserStorys"
    p.setFontSize(size=12, leading=None)
    p.drawString(45, salto, palabra8)
    for sp in sprints:
        palabra9 = "-Sprint: " + sp.nombre
        salto = salto - 20
        p.setFontSize(size=12, leading=None)
        p.drawString(75, salto, palabra9)
        palabra11 = "*Dias de Duracion : " + str(sp.dias_duracion)
        salto = salto - 25
        p.setFontSize(size=12, leading=None)
        p.drawString(100, salto, palabra11)
        variable = sp.id
        usn = UserStory.objects.filter(sprint_id=variable)
        for uss in usn:
            palabra10 = "--UserStory: " + str(uss.nombre)
            salto = salto - 15
            p.setFontSize(size=12, leading=None)
            p.drawString(150, salto, palabra10)

    p.showPage()
    p.save()
    return response