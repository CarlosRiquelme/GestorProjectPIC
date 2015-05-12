#-*-coding:utf-8-*-
from django.db import models
from django.contrib.auth.models import User, Group
from AdminProyectos.models import Proyecto


class RolUsuarioProyecto(models.Model):
    usuario=models.ForeignKey(User)
    proyecto=models.ForeignKey(Proyecto)
    rol=models.ForeignKey(Group, null=True)

def tienePermiso(self, permiso):
    for grupo in self.groups.all():
        for permisoUsuario in grupo.permissions.all():
            if permisoUsuario.codename == permiso:
                return True
    return False
User.add_to_class('tienePermiso', tienePermiso)

def tienePermisoProyecto(self, permisoCodename, id_proyecto):
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    for grupo in self.groups.filter(Proyecto=proyecto):
        for permisoUsuario in grupo.permissions.all():
            if permisoUsuario.codename == permisoCodename:
                return True
    return False
User.add_to_class('tienePermisoProyecto', tienePermisoProyecto)

def esDesarrollador(self):
    rol='Desarrollador'
    for grupo in self.groups.all():
        if grupo.name ==rol:
                return True
    return False

User.add_to_class('esDesarrollador', esDesarrollador)

def esLider(self):
    rol='ScrumMaster'
    for grupo in self.groups.all():
        if grupo.name ==rol:
                return True
    return False
User.add_to_class('esLider', esLider)

def esAdministrador(self):
    rol='Administrador'
    for grupo in self.groups.all():
        if grupo.name ==rol:
                return True
    return False
User.add_to_class('esAdministrador', esAdministrador)

def esVisitante(self):
    if self.puede_consultar_atributos() or self.puede_consultar_fases() or self.puede_consultar_proyectos() or self.puede_consultar_roles() or self.puede_consultar_tipodeitem() or self.puede_consultar_usuarios():
        return True
    return False
User.add_to_class('esVisitante', esVisitante)

def integraComite(self):
    rol='Integrante de Comite'
    for grupo in self.groups.all():
        if grupo.name ==rol:
                return True
    return False
User.add_to_class('integraComite', integraComite)

########################################################################################################################
#########################PERMISOS SOBRE USUARIOS########################################################################
########################################################################################################################
def puede_agregar_usuarios(self):
    permiso = 'add_user'
    return self.tienePermiso(permiso)
User.add_to_class('puede_agregar_usuarios', puede_agregar_usuarios)
def puede_modificar_usuarios(self):
    permiso = 'change_user'
    return self.tienePermiso(permiso)
User.add_to_class('puede_modificar_usuarios', puede_modificar_usuarios)
def puede_eliminar_usuarios(self):
    permiso = 'delete_user'
    return self.tienePermiso(permiso)
User.add_to_class('puede_eliminar_usuarios', puede_eliminar_usuarios)
def puede_consultar_usuarios(self):
    permiso = 'consulta_user'
    return self.tienePermiso(permiso)
User.add_to_class('puede_consultar_usuarios', puede_consultar_usuarios)
########################################################################################################################
#############PERMISOS SOBRE PROYECTOS###################################################################################
########################################################################################################################
def puede_agregar_proyectos(self):
    permiso = 'add_proyecto'
    return self.tienePermiso(permiso)
User.add_to_class('puede_agregar_proyectos', puede_agregar_proyectos)
def puede_modificar_proyectos(self):
    permiso = 'change_proyecto'
    return self.tienePermiso(permiso)
User.add_to_class('puede_modificar_proyectos', puede_modificar_proyectos)
def puede_eliminar_proyectos(self):
    permiso = 'delete_proyecto'
    return self.tienePermiso(permiso)
User.add_to_class('puede_eliminar_proyectos', puede_eliminar_proyectos)
def puede_consultar_proyectos(self):
    permiso = 'consulta_proyecto'
    return self.tienePermiso(permiso)
User.add_to_class('puede_consultar_proyectos', puede_consultar_proyectos)




