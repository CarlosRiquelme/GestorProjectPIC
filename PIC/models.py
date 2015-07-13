#-*-coding:utf-8-*-
from django.db import models
from django.contrib.auth.models import User, Group, Permission
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
def puede_agregar_proyectos(self):
    permiso = 'add_proyecto'
    return self.tienePermiso(permiso)

def esAdmin(self):
    rol='Administrador'
    for grupo in self.groups.all():
        print grupo
        if grupo.name == rol:
                return True
    return False
User.add_to_class('esAdmin', esAdmin)

def esScrumMaster(self):
    rol='ScrumMaster'
    for grupo in self.groups.all():
        print grupo
        if grupo.name == rol:
                return True
    return False
User.add_to_class('esScrumMaster',esScrumMaster)

def esEquipo(self,request):
    rol='Equipo'
    for grupo in self.groups.all():
        print grupo
        if grupo.name == rol:
                return True
    return False
User.add_to_class('esEquipo',esEquipo)
