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
from UserStory.models import UserStory
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

    return render_to_response('HtmlProyecto/proyectos.html',
                {'usuarioproyecto':usuarioproyecto,'user':user}, RequestContext(request))


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
    nombre=proyecto.nombre
    proyecto.delete()
    
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
    usuarioproyecto=RolUsuarioProyecto.objects.filter(proyecto_id=id_proyecto)
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
    userstorys = UserStory.objects.filter(sprint_id = id_sprint)
    sprint = Sprint.objects.get(pk=id_sprint)
    cantidad=0
    cantidad=Sprint_En_Proceso.objects.filter(sprint_id=id_sprint).count()
    sprint_proceso=Sprint_En_Proceso.objects.filter(sprint_id=id_sprint)
    print "cantidad: "+str(cantidad)
    v = [] #eje y en proceso
    v2 = [] # eje x
    v3 = [] # eje y estimado
    suma = 0
    for aux1 in userstorys:
        suma = suma + aux1.tiempo_estimado
    v3.append(suma)

    c=0
    contador=0
    for au in sprint_proceso:
        if cantidad !=0 and contador < cantidad:
            contador+=1
            aeiou = suma-au.horas_acumulada
            v3.append(aeiou)
            c=c+1


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

    return render_to_response('line-basic3/index.html',{'lista3':lista3,'lista2':lista1,'lista1':lista2})
def jo3(request,id_proyecto):
    """
    Funcion que grafica la estimacion del proyecto con lo que se esta desarrollando
    :param request:
    :param id_proyecto:
    :return:
    """
    userstorys=UserStory.objects.filter(proyecto_id=id_proyecto)

    # try:
    #     proyecto_proceso=Proyecto_En_Proceso.objects.get(proyecto_id=id_proyecto)
    # except ObjectDoesNotExist:
    #     proyecto_proceso=''
    # cantidad=0

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



    sprints = Sprint.objects.filter(proyecto_id=id_proyecto).order_by("fechaFin")
    for dato1 in sprints:
        suma = 0
        suma2 = 0
        for dato2 in userstorys:

            if(dato2.sprint_id == dato1.id):
                suma = suma + dato2.tiempo_estimado
                suma2 = suma2 + dato2.suma_trabajadas
        suma_estimacion_us = suma_estimacion_us - suma
        aux23 = aux23 - suma2
        lista1.append(suma_estimacion_us)
        lista3.append(str(dato1.fechaFin))
    print "sprint"
    print sprints
    proyecto_en_proceso=Proyecto_En_Proceso.objects.filter(proyecto_id=id_proyecto).order_by("fecha")

    resta=0
    fecha_max='2015-01-01'
    if proyecto_en_proceso.exists():
        for sp in sprints:
            for pep in proyecto_en_proceso.reverse():
                if sp.fechaInicio <= pep.fecha and pep.fecha <= sp.fechaFin:
                    if fecha_max < str(pep.fecha):
                        fecha_max=str(pep.fecha)
                        resta=aux_suma_estimacion_us-pep.horas_acumulada_sprint
                        lista4.append(resta)
    else:
        lista4.append(aux_suma_estimacion_us)
    #lista1 = [120, 100,90,80,70,60,50,40,30,20,10,0]
    lista2 = lista4
    #lista3 = ['1', ' 2', ' 3', ' 4', ' 5', ' 6',
    #            ' 7', ' 8', ' 9', ' 10', ' 11', ' 12']

    print "lista2"
    print lista2
    print "lista1"
    print lista1
    print "lista3"
    print lista3




    return render_to_response('line-basic2/index.html',{'lista3':lista3,'lista2':lista1,'lista1':lista2})

#################################################################################################
#############################     A PARTIR DE ACA LOS               #############################
#############################     DISTITNTOS REPORTES               #############################
#################################################################################################


def reporte01(request,id_proyecto):
    id_proyecto = id_proyecto
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = '; filename="somefilename.pdf"'

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.

    proyecto=Proyecto.objects.get(pk=id_proyecto)
    userstorys=UserStory.objects.filter(proyecto_id=id_proyecto)
    pu = RolUsuarioProyecto.objects.filter(proyecto_id=id_proyecto)
    user = User.objects.all()

    palabra = "Informe del Sistema Gestor Project PIC"
    palabra2 = "Cantidad de Trabajo en Curso por el Equipo"
    palabra3 = "Proyecto : " + proyecto.nombre
    palabra4 = "Estado : " + proyecto.estado
    palabra5 = "Scrum Master: " + str(proyecto.scrumMaster)
    palabra6 = "Equipo:"



    p.setFontSize(size=14, leading=None)
    p.drawString(200, 800, palabra)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 780, palabra2)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 760, palabra3)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 740, palabra4)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 720, palabra5)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 700, palabra6)

    c=0
    vect = []
    for a in pu:
        if(a.usuario_id != 1):
            userstorys2 = User.objects.get(id = a.usuario_id)
            vect.append(userstorys2)
            palabra7 = "             - " +str( userstorys2)
            p.setFontSize(size=12, leading=None)
            c=c+15
            a=700
            a=a-c
            p.drawString(45, a, palabra7)

    palabra8 = "User Storys:"
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 600, palabra8)


    a = 600
    ussss = UserStory.objects.filter(proyecto_id=id_proyecto).order_by('fecha_creacion')
    c=0
    d=0
    for cont in ussss:
        palabra9 =  "-Nombre :   " + str(cont.nombre)
        palabra10 = "-Usuario Responsable    :    "+ cont.usuario.username
        palabra11 = "*Tiempo Estimado:       " + str(cont.tiempo_estimado)
        palabra12 = "*Tiempo Trabajado:      " + str(cont.tiempo_trabajado)
        a = a - 20
        b = a - 15
        c = b - 15
        d = c - 15
        p.setFontSize(size=12, leading=None)
        p.drawString(100, a, palabra9)
        p.setFontSize(size=12, leading=None)
        p.drawString(100, b, palabra10)
        p.setFontSize(size=12, leading=None)
        p.drawString(150, c, palabra11)
        p.setFontSize(size=12, leading=None)
        p.drawString(150, d, palabra12)
        a = d



    # Close the PDF object cleanly.
    p.showPage()
    p.save()




    # Get the value of the BytesIO buffer and write it to the response.
    # pdf = buffer.getvalue()



    #buffer.close()
    #response.write(pdf)
    return response

def lista_de_reportes(request,id_proyecto):
    lista3 = id_proyecto
    return render_to_response('HtmlReportes/ReportePrincipal.html',{'lista3':lista3})



def reporte02(request,id_proyecto):
    id_proyecto = id_proyecto
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = '; filename="somefilename.pdf"'

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    TPendientes = UserStory.objects.filter(proyecto_id=id_proyecto).filter(estado="CREADO")
    TFinalizados = UserStory.objects.filter(proyecto_id=id_proyecto).filter(estado="FINALIZADO")
    TenCursos = UserStory.objects.filter(proyecto_id=id_proyecto).exclude(estado="CREADO").exclude(estado="FINALIZADO").exclude(estado="CANCELADO")
    proyecto=Proyecto.objects.get(pk=id_proyecto)
    userstorys=UserStory.objects.filter(proyecto_id=id_proyecto)
    UsuariosProyectos = RolUsuarioProyecto.objects.filter(proyecto_id=id_proyecto)
    for jo in UsuariosProyectos:
        user = User.objects.filter(id=jo.usuario_id)

    palabra = "Informe del Sistema Gestor Project PIC"
    palabra2 = "Cantidad de Trabajo por Usuario Pendiente, en Curso y Finalizados."
    palabra3 = "Proyecto : " + proyecto.nombre
    palabra4 = "Estado : " + proyecto.estado
    palabra5 = "Scrum Master: " + str(proyecto.scrumMaster)
    palabra6 = "Equipo:"



    p.setFontSize(size=14, leading=None)
    p.drawString(200, 800, palabra)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 780, palabra2)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 760, palabra3)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 740, palabra4)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 720, palabra5)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 700, palabra6)

    c=0
    vect = [] #vector que contiene us
    vect2 = [] # vector que contiene usuarios
    for a in UsuariosProyectos:
        if(a.usuario_id != 1):
            userstorys2 = User.objects.get(id = a.usuario_id)
            vect.append(userstorys2)
            vect2.append(a.usuario_id)
            palabra7 = "             - " +str( userstorys2)
            p.setFontSize(size=12, leading=None)
            c=c+15
            a=700
            a=a-c
            p.drawString(60, a, palabra7)


    salto = 600



    for a in UsuariosProyectos:
        if(a.usuario_id != 1):
            userstorys2 = User.objects.get(id = a.usuario_id)
            vect.append(userstorys2)
            vect2.append(a.usuario_id)
            palabra9 = "Usuario: " +str( userstorys2)
            salto = salto - 15
            p.setFontSize(size=10, leading=None)
            p.drawString(45, salto, palabra9)

            palabra10 = "Trabajos Pendientes:  "
            salto = salto - 15
            p.setFontSize(size=8, leading=None)
            p.drawString(100, salto, palabra10)
            for pen in TPendientes:
                if(pen.usuario_id == a.usuario_id):
                    palabra11 = "                  -" + str(pen.nombre)
                    salto = salto - 15
                    p.setFontSize(size=8, leading=None)
                    p.drawString(150, salto, palabra11)





            palabra12 = "Trabajos Finalizados:  "
            salto = salto - 15
            p.setFontSize(size=8, leading=None)
            p.drawString(100, salto, palabra12)
            for pen in TFinalizados:
                if(pen.usuario_id == a.usuario_id):
                    palabra13 = "                  -" + str(pen.nombre)
                    salto = salto - 15
                    p.setFontSize(size=8, leading=None)
                    p.drawString(150, salto, palabra13)
            palabra14 = "Trabajos En Cursos:  "
            salto = salto - 15
            p.setFontSize(size=8, leading=None)
            p.drawString(100, salto, palabra14)
            for pen in TenCursos:
                if(pen.usuario_id == a.usuario_id):
                    palabra15 = "                  -" + str(pen.nombre)
                    salto = salto - 15
                    p.setFontSize(size=8, leading=None)
                    p.drawString(150, salto, palabra15)




    # Close the PDF object cleanly.
    p.showPage()
    p.save()




    # Get the value of the BytesIO buffer and write it to the response.
    # pdf = buffer.getvalue()



    #buffer.close()
    #response.write(pdf)
    return response

def reporte03(request,id_proyecto):
    id_proyecto = id_proyecto
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = '; filename="somefilename.pdf"'

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.

    proyecto=Proyecto.objects.get(pk=id_proyecto)
    userstorys=UserStory.objects.filter(proyecto_id=id_proyecto)
    pu = RolUsuarioProyecto.objects.filter(proyecto_id=id_proyecto)
    user = User.objects.all()

    palabra = "Informe del Sistema Gestor Project PIC"
    palabra2 = "Lista clasificada por orden de prioridad de todas las actividades para completar el proyecto."
    palabra3 = "Proyecto : " + proyecto.nombre
    palabra4 = "Estado : " + proyecto.estado
    palabra5 = "Scrum Master: " + str(proyecto.scrumMaster)
    palabra6 = "Equipo:"




    p.setFontSize(size=14, leading=None)
    p.drawString(200, 800, palabra)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 780, palabra2)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 760, palabra3)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 740, palabra4)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 720, palabra5)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 700, palabra6)

    c=0
    vect = []
    for a in pu:
        if(a.usuario_id != 1):
            userstorys2 = User.objects.get(id = a.usuario_id)
            vect.append(userstorys2)
            palabra7 = "             - " +str( userstorys2)
            p.setFontSize(size=12, leading=None)
            c=c+15
            a=700
            a=a-c
            p.drawString(45, a, palabra7)

    palabra8 = "Actividades:"
    p.setFontSize(size=14, leading=None)
    p.drawString(45, 600, palabra8)
    salto = 600

    actividades=Actividad.objects.filter(proyecto_id=id_proyecto)

    c=0
    for i in actividades:
        c=c+1
        palabra9 = "-Nombre de la Actividad: " + str(i.nombre)
        palabra10 = "-Prioridad: " + str(i.secuencia)
        salto = salto -20
        p.setFontSize(size=12, leading=None)
        p.drawString(150, salto, palabra9)
        salto = salto -15
        p.setFontSize(size=12, leading=None)
        p.drawString(150, salto, palabra10)






    # Close the PDF object cleanly.
    p.showPage()
    p.save()




    # Get the value of the BytesIO buffer and write it to the response.
    # pdf = buffer.getvalue()



    #buffer.close()
    #response.write(pdf)
    return response

def reporte04(request,id_proyecto):
    id_proyecto = id_proyecto
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = '; filename="somefilename.pdf"'

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.

    proyecto=Proyecto.objects.get(pk=id_proyecto)
    sprints=Sprint.objects.filter(proyecto_id=id_proyecto)
    userstorys=UserStory.objects.filter(proyecto_id=id_proyecto)
    pu = RolUsuarioProyecto.objects.filter(proyecto_id=id_proyecto)
    user = User.objects.all()

    palabra = "Informe del Sistema Gestor Project PIC"
    palabra2 = "Lista de Tiempo estimado"
    palabra3 = "Proyecto : " + proyecto.nombre
    palabra4 = "Estado : " + proyecto.estado
    palabra5 = "Scrum Master: " + str(proyecto.scrumMaster)
    palabra6 = "Equipo:"



    p.setFontSize(size=14, leading=None)
    p.drawString(200, 800, palabra)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 780, palabra2)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 760, palabra3)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 740, palabra4)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 720, palabra5)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 700, palabra6)

    c=0
    vect = []
    for a in pu:
        if(a.usuario_id != 1):
            userstorys2 = User.objects.get(id = a.usuario_id)
            vect.append(userstorys2)
            palabra7 = "             - " +str( userstorys2)
            p.setFontSize(size=12, leading=None)
            c=c+15
            a=700
            a=a-c
            p.drawString(45, a, palabra7)

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





    # Close the PDF object cleanly.
    p.showPage()
    p.save()




    # Get the value of the BytesIO buffer and write it to the response.
    # pdf = buffer.getvalue()



    #buffer.close()
    #response.write(pdf)
    return response
def reporte05(request,id_proyecto):
    id_proyecto = id_proyecto
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = '; filename="somefilename.pdf"'

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.

    proyecto=Proyecto.objects.get(pk=id_proyecto)
    userstorys=UserStory.objects.filter(proyecto_id=id_proyecto)
    pu = RolUsuarioProyecto.objects.filter(proyecto_id=id_proyecto)
    user = User.objects.all()

    palabra = "Informe de Sistema Gestor Project PIC"
    palabra2 = "Backlog de Producto"
    palabra3 = "Proyecto : " + proyecto.nombre
    palabra4 = "Estado : " + proyecto.estado
    palabra5 = "Scrum Master: " + str(proyecto.scrumMaster)
    palabra6 = "Equipo:"


    p.setFontSize(size=14, leading=None)
    p.drawString(200, 800, palabra)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 780, palabra2)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 760, palabra3)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 740, palabra4)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 720, palabra5)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 700, palabra6)

    c=0
    vect = []
    for a in pu:
        if(a.usuario_id != 1):
            userstorys2 = User.objects.get(id = a.usuario_id)
            vect.append(userstorys2)
            palabra7 = "             - " +str( userstorys2)
            p.setFontSize(size=12, leading=None)
            c=c+15
            a=700
            a=a-c
            p.drawString(45, a, palabra7)

    palabra8 = "User Storys"
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 600, palabra8)


    a = 600
    ussss = UserStory.objects.filter(proyecto_id=id_proyecto).order_by('tiempo_estimado')
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



    # Close the PDF object cleanly.
    p.showPage()
    p.save()




    # Get the value of the BytesIO buffer and write it to the response.
    # pdf = buffer.getvalue()



    #buffer.close()
    #response.write(pdf)
    return response

def reporte06(request,id_proyecto):
    id_proyecto = id_proyecto
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = '; filename="somefilename.pdf"'

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.

    proyecto=Proyecto.objects.get(pk=id_proyecto)
    userstorys=UserStory.objects.filter(proyecto_id=id_proyecto)
    sprints = Sprint.objects.filter(proyecto_id=id_proyecto)
    pu = RolUsuarioProyecto.objects.filter(proyecto_id=id_proyecto)
    user = User.objects.all()

    palabra = "Informe de Sistema Gestor Project PIC"
    palabra2 = "Backlog de Sprints"
    palabra3 = "Proyecto : " + proyecto.nombre
    palabra4 = "Estado : " + proyecto.estado
    palabra5 = "Scrum Master: " + str(proyecto.scrumMaster)
    palabra6 = "Equipo:"



    p.setFontSize(size=14, leading=None)
    p.drawString(200, 800, palabra)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 780, palabra2)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 760, palabra3)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 740, palabra4)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 720, palabra5)
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 700, palabra6)

    c=0
    vect = []
    for a in pu:
        if(a.usuario_id != 1):
            userstorys2 = User.objects.get(id = a.usuario_id)
            vect.append(userstorys2)
            palabra7 = "             - " +str( userstorys2)
            p.setFontSize(size=12, leading=None)
            c=c+15
            a=700
            a=a-c
            p.drawString(45, a, palabra7)

    palabra8 = "Sprints y sus UserStorys"
    p.setFontSize(size=12, leading=None)
    p.drawString(45, 600, palabra8)
    salto = 600
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






    # Close the PDF object cleanly.
    p.showPage()
    p.save()




    # Get the value of the BytesIO buffer and write it to the response.
    # pdf = buffer.getvalue()



    #buffer.close()
    #response.write(pdf)
    return response