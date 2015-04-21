from django.db import models
from django.contrib.auth.models import User, Group


# Create your models here.
#prueba de branch
class Usuario_rol(models.Model):
    usuario = models.ForeignKey(User)
    rol = models.ForeignKey(Group)

class Proyecto(models.Model):
    nombre = models.CharField(max_length=60)
    descripcion = models.CharField(max_length=120)
    fechaCreacion = models.DateTimeField('Fecha de Creacion')
    fechaInicio = models.DateTimeField('Fecha de Inicio')
    fechaFin = models.DateTimeField('Fecha de Fin')
    duracionEstimada = models.CharField(max_length=20)
    estado = models.CharField(max_length=40)
    usuario_rol = models.ManyToManyField(Usuario_rol, related_name='proyectos')
    def __unicode__(self):
        return self.nombre  

class Flujo(models.Model):
	nombre=models.CharField(max_length=60)
	tiempo_estimado=models.IntegerField()
	estado=models.CharField(max_length=40)
	proyecto = models.ForeignKey(Proyecto)
	def __unicode__(self):
		return self.nombre   

