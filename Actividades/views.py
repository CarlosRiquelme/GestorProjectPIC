# from mx.DateTime.DateTime import today
# from django.contrib.auth.models import User
# from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# from django.shortcuts import render_to_response
# from django.template.context import RequestContext
# from django.http import HttpResponseRedirect
# from django.views.generic.dates import timezone_today
# from Actividades.models import Actividad
# #from projectx.globales import execute_query
# from AdminProyectos.models import Proyecto
# from Flujo.models import Flujo
# from django.contrib import messages
#
#
# def actividad_flujo(request, id_flujo):
#     flujo=Flujo.objects.get(pk=id_flujo)
#     actividades=Actividad.objects.filter(flujo_id=id_flujo).order_by('secuencia')
#     lista_actividades=Actividad.objects.filter(estado='PROGRAMADO').exclude(flujo_id=id_flujo).order_by('nombre')
#     if request.method == 'POST':
#         id_actividad=request.POST.get('id_actividad','')
#         if id_actividad != "":
#             actividad=Actividad.objects.get(pk=id_actividad)
#             nombre=request.POST.get('nombre','')
#             if nombre !="":
#
#                 fase.nombre=nombre
#                 fase.descripcion=descripcion
#                 fase.estado="INICIADO"
#                 if fase.nombre == "":
#                     messages.success(request,"Fase creada con exito!")
#                 else:
#                     messages.success(request,"Fase editada con exito!")
#             fase.save()
#
#
#
#     return render_to_response('HtmlFases/fasesflujo.html',
#     {'fases':fases,'flujo':flujo,'lista_fases':lista_fases,'ESTADOS_FASE':ESTADOS_FASE}, context_instance=RequestContext(request))
#
#
# def actividad(request, id_actividad,id_flujo):
#     actividad=Actividad.objects.get(pk=id_actividad)
#     if actividad.nombre == None:
#         modo='Crear'
#     else:
#         modo='Editar'
#
#     msg=''
#     if request.method=='POST':
#          nombre=request.POST.get('nombre','')
#          aux=Actividad.objects.filter(nombre=nombre).count()
#          if aux >1:
#             msg='Ya existe una Actividad con el mismo nombre'
#             messages.warning(request,msg)
#
#             return render_to_response('HtmlActividad/editActividad.html',{'fase':actividad,'modo':modo,'msg':msg,'id_proyecto':id_flujo},context_instance=RequestContext(request))
#          fecha=timezone_today()
#          actividad.nombre=nombre
#          actividad.descripcion=descripcion
#          actividad.estado='INICIADO'
#          actividad.fecha_creacion=fecha
#          actividad.save()
#          messages.success(request,"Fase Modificada con exito!")
#
#          return HttpResponseRedirect('/proyecto/fases/'+str(id_proyecto))
#
#     estados=ESTADOS_FASE
#
#     return render_to_response('HtmlFases/editfase.html',{'fase':fase,'modo':modo,'msg':msg,'estados':['asdf','adsf'],'id_proyecto':id_proyecto},context_instance=RequestContext(request))
