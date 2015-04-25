#-*-coding:utf-8-*-
from django.db import models
from django.contrib.auth.models import User, Group


# Create your models here.
#prueba de branch

class Usuario_rol(models.Model):
    usario_Rol=models.CharField(max_length=40)
    usuario = models.ForeignKey(User)
    rol = models.ForeignKey(Group)
    class Meta:
        verbose_name = "Asignar Rol a User"
        verbose_name_plural = "Asignar Rol a User"
    def __unicode__(self):
        return self.usario_Rol



PROYECTOS_ESTADOS = (
    ('EN-ESPERA', 'EN-ESPERA'),
    ('EN-DESARROLLO', 'EN-DESARROLLO'),
    ('FINALIZADO', 'FINALIZADO'),
)

FLUJOS_ESTADOS = (
    ('EN-ESPERA', 'EN-ESPERA'),
    ('EN-DESARROLLO', 'EN-DESARROLLO'),
    ('FINALIZADO', 'FINALIZADO'),
)

# class Usuario_Rol(models.Model):
#     usuario = models.ForeignKey(User)
#     rol= models.ForeignKey(Group)
#     # class Meta:
#     #     verbose_name = "Asignar Rol a User"
#     #     verbose_name_plural = "Asignar Rol a User"

class Proyecto(models.Model):
    """
    *Modelo para la clase* ``Proyecto`` *, en el cual se encuentras todos los atributos de un proyecto:*
        + *Nombre*: Nombre del Proyecto
        + *Descripción*: Breve reseña del proyecto
        + *Fecha de Creación*: Fecha de creación del proyecto
        + *Fecha de Inicio*: Fecha de inicio del proyecto
        + *Fecha de Fin*: Fecha estimada de finalización del proyecto
        + *Duracion Estimada*: Tiempo Estimado de finalizacion del proyecto en semanas
        + *Estado*: Los estados posibles del Proyecto
        + *Usuarios*: Usuarios que posee un proyecto.
    """

    """
    Esta clase representa a los proyectos de desarrollo de software
    que seran creados en la aplicacion.

    Sus atributos seran:
     - Nombre
     - Descripcion
     - Fecha de creacion
     - Fecha de inicio del proyecto
     - Fecha de finalizacion del proyecto
     - Duracion estimada del proyecto
     - Estado: que podria ser en espera, en desarrollo o finalizado
     - Scrum master el usuario lider


    """
    nombre = models.CharField(max_length=60)
    descripcion = models.CharField(max_length=120)
    fechaCreacion = models.DateTimeField('Fecha de Creacion')
    fechaInicio = models.DateTimeField('Fecha de Inicio')
    fechaFin = models.DateTimeField('Fecha de Fin')
    duracionEstimada = models.CharField(max_length=20)
    estado = models.CharField(max_length=40, choices=PROYECTOS_ESTADOS, default='EN-ESPERA')
    scrumMaster=models.ForeignKey(User,null=True)
    usuario_rol = models.ManyToManyField(Usuario_rol, related_name='proyectos')

    def __unicode__(self):
        return self.nombre


class Flujo(models.Model):

    """
    *Modelo para la clase* ``Flujo`` *, en el cual se encuentras todos los atributos de un flujo:*
        + *Nombre*: Nombre del Proyecto
        + *Tiempo Estimado*: Tiempo estimado de la finalizacion del flujo
        + *Estado*: Los estados posibles del Flujo
        + *Proyecto*: Proyecto al cual pertenece el Flujo.

    """

    """
    Esta clase representa a los flujos de desarrollo de software
    que seran creados en la aplicacion.

    Sus atributos seran:
     - Nombre
     - Duracion estimada del proyecto
     - Estado: que podria ser en espera, en desarrollo o finalizado

    """


    nombre=models.CharField(max_length=60)
    tiempo_estimado=models.IntegerField()
    estado=models.CharField(max_length=40,choices=False,default='EN-ESPERA')
    proyecto = models.ForeignKey(Proyecto, null=True)
    def __unicode__(self):
        return self.nombre

class User_Story(models.Model):

    """
    Esta clase representa a los User Storys que tendra la aplicacion.

    Sus atributos seran:
     - Nombre
     - Descripcion
     - Fecha de creacion
     - Tiempo acumulado
     - Fecha de inicio
     - Fecha de finalizacion
     - Duracion estimada
     - Estado: que podria ser en espera, en desarrollo o finalizado
     - y sus respectivas referencias

    """


    nombre=models.CharField(max_length=40)
    descripcion=models.TextField(max_length=120)
    tiempo_estimado=models.IntegerField()
    tiempo_trabajado=models.IntegerField(default=0)
    fecha_inicio=models.DateTimeField('Fecha de Inicio')
    fecha_fin=models.DateTimeField('Fecha Fin')
    user=models.ForeignKey(User)
    proyecto=models.ForeignKey(Proyecto)
    flujo=models.ForeignKey(Flujo)
    activo=models.BooleanField(default=False)
    sprint=models.ForeignKey('Sprint')
    class Meta:
        verbose_name = "User Story"
        verbose_name_plural = "User Story"
    def __unicode__(self):
        return self.nombre


class Sprint(models.Model):
    """
    Esta clase representa a los Sprint

    Sus atributos seran:
     - Nombre
     - Fecha de creacion
     - Fecha de inicio
     - Fecha fin estimada
     - Tiempo estimado

    """
    nombre = models.CharField(max_length=60)
    fechaCreacion = models.DateTimeField('Fecha de Creacion')
    fechaInicio = models.DateTimeField('Fecha de Inicio')
    fechaFinEstimado = models.DateTimeField('Fecha de Fin Estimado')
    #user_story = models.ForeignKey(User_Story)
    tiempoEstimado = models.IntegerField()
    def __unicode__(self):
        return self.nombre

class Comentario(models.Model):
    """
    Esta clase representa a los comentarios que se agregaran a cada user story

    Sus atributos seran:
     - Titulo
     - Contenido
     - Fecha del comentario
     - User Story asociado
     - Hora dedicada al user story en el dia

    """
    titulo=models.CharField(max_length=20)
    contenido=models.TextField(max_length=200)
    fecha=models.DateTimeField(auto_now=True)
    user_story=models.ForeignKey(User_Story)
    hora_trabajada=models.IntegerField()
    def __unicode__(self):
        return self.titulo


