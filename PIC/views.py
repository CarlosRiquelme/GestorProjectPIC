
from django.db.models import Q
from django.contrib.auth.models import User, Group, Permission
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from PIC.forms import RegistrationForm, EditUserForm, GroupForm
from django.contrib import messages
from django.shortcuts import render_to_response, get_object_or_404
from AdminProyectos.models import Proyecto
from django.contrib.auth.decorators import login_required, user_passes_test



# @login_required(login_url='/admin/login/?next=/admin/')
# def prueba(request):
#     print "hola mundo"

# # Create your views here.
# #hola bebe
#
# def crear_user_story(request):
#     context=RequestContext(request)
#     register=False
#     if request.method=='POST':
#         user_story_form=User_Story(data=request.POST)
#         if user_story_form.is_valid():
#             user_story_form.clean()
#             nombre=user_story_form.cleaned_data['nombre']
#             descripcion=user_story_form.cleaned_data['descripcion']
#             tiempo_estimado=user_story_form.cleaned_data['tiempo_estimado']
#             tiempo_trabajado=user_story_form.cleaned_data['tiempo_trabajado']
#             fecha_inicio=user_story_form.cleaned_data['fecha_inicio']
#             fecha_fin=user_story_form.cleaned_data['fecha_fin']
#             #user=user_story_form.cleaned_data['user']
#             #proyecto=user_story_form.cleaned_data['proyecto']
#
#             user_story=User_Story()
#             user_story.nombre=nombre
#             user_story.descripcion=descripcion
#             user_story.tiempo_estimado=tiempo_estimado
#             user_story.tiempo_estimado=tiempo_estimado
#             user_story.tiempo_trabajado=tiempo_trabajado
#             user_story.fecha_inicio=fecha_inicio
#             user_story.fecha_fin=fecha_fin
#             #user_story.user=user
#             #user_story.proyecto=proyecto
#             user_story.activo=False
#            # user_story.flujo=
#             user_story.save()
#             register=True
#         else:
#             print user_story_form.erros
#     else:
#         user_story_form=User_StoryForm()
#     return render_to_response('crear.html',{'user_story_form':user_story_form, 'register':register},context)
#

def nuevo_usuario(request):
    """
    Crea un nuevo Usuario con sus atributos proveidos por el
    usuario y el Sistema autogenera los demas atributos
    """
    user=request.user
    # if not user.is_superuser:
    #       return HttpResponseRedirect('/sinpermiso/')

    if request.method=='POST':
        formulario= RegistrationForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/usuarios')
    else:
        formulario= RegistrationForm(request.POST)
    return render_to_response('UsuariosHtml/nuevousuario.html',{'formulario':formulario}, context_instance=RequestContext(request))


def editar_usuario(request, id_user):
     user=request.user
     if not user.is_superuser:
          return HttpResponseRedirect('/sinpermiso/')
     usuario=User.objects.get(pk=id_user)
     if request.method=='POST':
        formulario =EditUserForm(request.POST,instance=usuario)
        if formulario.is_valid():
            formulario.save()
            messages.success(request,"Usuario Modificado con exito!")
            return HttpResponseRedirect('/usuarios')
        else:
            messages.warning(request,"Debe completar los campos obligatorios!")
     else:
        formulario = EditUserForm(instance=usuario)
     return render_to_response('UsuariosHtml/editarusuario.html',{'formulario':formulario}, context_instance=RequestContext(request))

def activar_usuario(request, id_user):
    """
    Vuelve activar a un Usuario que anteriomente fue desactivado
    """
    user=request.user
    if not user.is_superuser:
          return HttpResponseRedirect('/sinpermiso/')
    usuario=User.objects.get(pk=id_user)
    usuario.is_active=True
    usuario.save()
    return HttpResponseRedirect('/usuarios')



def usuarios(request):
    buscar=''
    if request.method == 'GET':
        buscar=request.GET.get('buscar','')
    usuarios_list = User.objects.filter(Q(username__icontains=buscar)|Q(first_name__icontains=buscar))
    paginator = Paginator(usuarios_list, 10) # Show 25 contacts per page

    page = request.GET.get('page','')
    try:
        page=int(page)
    except:
        page=1
    try:
        usuarios = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        usuarios = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        usuarios = paginator.page(paginator.num_pages)

    return render_to_response('UsuariosHtml/usuarios.html',
                {'objetos':usuarios,'page_range':paginator.page_range,'total':usuarios_list.count(),
                 'page':int(page),'buscar':buscar,'placeholder':'Username o Nombre'
                                                                #'roles':roles
                                                                }, RequestContext(request))

def desactivar_usuario(request,id_user):
    """
    Desactiva al usuario de la lista
    """

    usuario=User.objects.get(pk=id_user)
    usuario.is_active=False
    usuario.save()
    return HttpResponseRedirect('/usuarios')

def crearRol(request):
    """ Recibe un request, obtiene el formulario con los datos del rol a crear
    que consta de un nombre y una lista de permisos. Y registra el nuevo rol.

    @type request: django.http.HttpRequest
    @param request: Contiene informacion sobre la solic. web actual que llamo a esta vista

    @rtype: django.http.HttpResponse
    @return: creacionRol.html, mensaje de exito

    @author: Gabriela Vazquez

    """
    #valor booleano para llamar al template cuando el registro fue correcto
    registered = False
    if request.method == 'POST':
        group_form = GroupForm(request.POST)

        if group_form.is_valid():
            # formulario validado correctamente
            group_form.save()
             #Actualiza la variable para llamar al template cuando el registro fue correcto
            registered = True

    else:
        # formulario inicial
        group_form = GroupForm()
    return render_to_response('roles/creacionRol.html', { 'group_form': group_form, 'registered': registered}, context_instance=RequestContext(request))


def roles(request):
    """ Recibe un request, luego lista los roles existentes en el sistema

    @type request: django.http.HttpRequest
    @param request: Contiene informacion sobre la solicitud web actual que llamo a esta vista

    @rtype: django.http.HttpResponse
    @return: roles.html, mensaje de exito

    @author: Gabriela Vazquez

    """

    grupos = Group.objects.all()
    return render_to_response('roles/roles.html', {'lista_roles': grupos}, context_instance=RequestContext(request))


def consultar_roles(request, id_rol):
    """ Recibe un request y un identificador del rol que se desea consultar, se
    busca en la base de datos y se muestra.

    @type request: django.http.HttpRequest
    @param request: Contiene informacion sobre la solicitud web actual que llamo a esta vista

    @type id_rol: integer
    @param id_rol: Identificador unico del Rol que se quiere consultar

    @rtype: django.http.HttpResponse
    @return: consultarRol.html

    @author: Gabriela Vazquez

    """

    #Http404 si el objeto no existe.
    rol = get_object_or_404(Group, pk=id_rol)
    #filtramos todos los permisos que tengan como id grupo el pasado como parametro
    list_permisos = Permission.objects.filter(group__id=id_rol)
    return render_to_response('roles/consultarRol.html', {'rol':rol, 'permisos':list_permisos}, context_instance=RequestContext(request))


def eliminar_rol (request , id_rol):
    """ Recibe un request y un identificador del rol que se desea eliminar, se
    busca en la base de datos y se elimina logicamente.

    @type request: django.http.HttpRequest
    @param request: Contiene informacion sobre la solicitud web actual que llamo a esta vistar

    @type id_rol: integer
    @param id_rol: Identificador unico del Rol que se quiere eliminar

    @rtype: django.http.HttpResponse
    @return: eliminarRol.html

    @author: Gabriela Vazquez

    """
    #editar de acuerdo a nuevas necesidades
    rol = get_object_or_404(Group, pk=id_rol)
    rol.delete()
    if rol.name == 'Admin':
        messages.add_message(request, settings.DELETE, "El rol administrador no puede ser eliminado")

    list_grupos = Group.objects.all()
    return render_to_response('roles/eliminarRol.html', {'datos': list_grupos}, context_instance=RequestContext(request))

def modificar_rol (request , id_rol):
    """ Recibe un request y un identificador del rol que se desea modificar, se
    busca en la base de datos. Presenta los datos del rol en un formulario
    y luego se guardan los cambios realizados

    @type request: django.http.HttpRequest
    @param request: Contiene informacion sobre la solicitud web actual que llamo a esta vistar

    @type id_rol: integer
    @param id_rol: Identificador unico del Rol que se quiere modificar

    @rtype: django.http.HttpResponse
    @return: modificarRol.html

    @author: Gabriela Vazquez

    """
    #editar de acuerdo a nuevas necesidades
    rol = Group.objects.get(id=id_rol)
    if request.method == 'POST':
        rol_form = GroupForm(request.POST, instance=rol)

        if rol_form.is_valid():
            rol_form.save()
            #return HttpResponse("Rol registrado correctamente")
            template_name = './roles/rol_modificado.html'
            return render(request, template_name)
    else:
        rol_form = GroupForm(instance=rol)

    return render_to_response('roles/modificarRol.html',{ 'rol': rol_form, 'dato': rol}, context_instance=RequestContext(request))

