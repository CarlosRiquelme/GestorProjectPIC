#-*-coding:utf-8-*-
from django.db import models
from django.contrib.auth.models import User, Group


# Create your models here.
#prueba de branch
#
# PROYECTOS_ESTADOS = (
#     ('EN-ESPERA', 'EN-ESPERA'),
#     ('EN-DESARROLLO', 'EN-DESARROLLO'),
#     ('FINALIZADO', 'FINALIZADO'),
# )
#
# FLUJOS_ESTADOS = (
#     ('EN-ESPERA', 'EN-ESPERA'),
#     ('EN-DESARROLLO', 'EN-DESARROLLO'),
#     ('FINALIZADO', 'FINALIZADO'),
# )
#
# class Usuario_Rol(models.Model):
#     usuario = models.ForeignKey(User)
#     rol= models.ForeignKey(Group)
#     # class Meta:
#     #     verbose_name = "Asignar Rol a User"
#     #     verbose_name_plural = "Asignar Rol a User"
#
# class Proyecto(models.Model):
#     """
#     *Modelo para la clase* ``Proyecto`` *, en el cual se encuentras todos los atributos de un proyecto:*
#         + *Nombre*: Nombre del Proyecto
#         + *Descripción*: Breve reseña del proyecto
#         + *Fecha de Creación*: Fecha de creación del proyecto
#         + *Fecha de Inicio*: Fecha de inicio del proyecto
#         + *Fecha de Fin*: Fecha estimada de finalización del proyecto
#         + *Duracion Estimada*: Tiempo Estimado de finalizacion del proyecto en semanas
#         + *Estado*: Los estados posibles del Proyecto
#         + *Usuarios*: Usuarios que posee un proyecto.
#     """
#     nombre = models.CharField(max_length=60)
#     descripcion = models.CharField(max_length=120)
#     fechaCreacion = models.DateTimeField('Fecha de Creacion')
#     fechaInicio = models.DateTimeField('Fecha de Inicio')
#     fechaFin = models.DateTimeField('Fecha de Fin')
#     duracionEstimada = models.CharField(max_length=20)
#     estado = models.CharField(max_length=40, choices=PROYECTOS_ESTADOS, default='EN-ESPERA')
#     rol_usuario = models.ManyToManyField(Usuario_Rol, related_name='proyectos')
#     scrumMaster=models.ForeignKey(User)
#     def __unicode__(self):
#         return self.nombre
#
#
# class Flujo(models.Model):
#
#     """
#     *Modelo para la clase* ``Flujo`` *, en el cual se encuentras todos los atributos de un flujo:*
#         + *Nombre*: Nombre del Proyecto
#         + *Tiempo Estimado*: Tiempo estimado de la finalizacion del flujo
#         + *Estado*: Los estados posibles del Flujo
#         + *Proyecto*: Proyecto al cual pertenece el Flujo.
#     """
#
#     nombre=models.CharField(max_length=60)
#     tiempo_estimado=models.IntegerField()
#     estado=models.CharField(max_length=40,choices=False,default='EN-ESPERA')
#     proyecto = models.ForeignKey(Proyecto)
#     def __unicode__(self):
# 		return self.nombre
#
# class user_story(models.Model):
#     nombre = models.CharField(max_length=60)
#     fechaCreacion = models.DateTimeField('Fecha de Creacion')
#     fechaInicio = models.DateTimeField('Fecha de Inicio')
#     fechaFin = models.DateTimeField('Fecha de Fin')
#     duracionEstimada = models.CharField(max_length=20)
#     estado = models.CharField(max_length=40, choices=PROYECTOS_ESTADOS, default='EN-ESPERA')
#

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
    rol='Lider de Proyecto'
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




