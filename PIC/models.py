from django.db import models
from django.contrib.auth.models import User, Group


# Create your models here.
#prueba de branch
<<<<<<< HEAD
class Usuario_rol(models.Model):
    usuario = models.ForeignKey(User)
    rol = models.ForeignKey(Group)
=======


>>>>>>> 05c1e52ab761cc08c528e9799f4e4e9c78cbaaa0

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
    nombre = models.CharField(max_length=60)
    descripcion = models.CharField(max_length=120)
    fechaCreacion = models.DateTimeField('Fecha de Creacion')
    fechaInicio = models.DateTimeField('Fecha de Inicio')
    fechaFin = models.DateTimeField('Fecha de Fin')
    duracionEstimada = models.CharField(max_length=20)
    estado = models.CharField(max_length=40)
    usuario_rol = models.ManyToManyField(Usuario_rol, related_name='proyectos')
    def __unicode__(self):
<<<<<<< HEAD
        return self.nombre  

=======
        return self.nombre

#<<<<<<< HEAD

    
#=======
>>>>>>> 05c1e52ab761cc08c528e9799f4e4e9c78cbaaa0
class Flujo(models.Model):

    """
    *Modelo para la clase* ``Flujo`` *, en el cual se encuentras todos los atributos de un flujo:*
        + *Nombre*: Nombre del Proyecto
        + *Tiempo Estimado*: Tiempo estimado de la finalizacion del flujo
        + *Estado*: Los estados posibles del Flujo
        + *Proyecto*: Proyecto al cual pertenece el Flujo.
    """

    nombre=models.CharField(max_length=60)
    tiempo_estimado=models.IntegerField()
    estado=models.CharField(max_length=40)
    proyecto = models.ForeignKey(Proyecto)
    def __unicode__(self):
		return self.nombre   
<<<<<<< HEAD

=======
#>>>>>>> cf64be24e8fb6eee3e0fc5f538b152687c3fa45d
>>>>>>> 05c1e52ab761cc08c528e9799f4e4e9c78cbaaa0
