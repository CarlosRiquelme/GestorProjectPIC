from django.db import models
import datetime
from django.contrib.auth.models import User


# Create your models here.
#prueba de branch
class Proyecto(models.Model):
    nombre = models.CharField(max_length=60)
    descripcion = models.CharField(max_length=120)
    fechaCreacion = models.DateTimeField('Fecha de Creacion')
    fechaInicio = models.DateTimeField('Fecha de Inicio')
    fechaFin = models.DateTimeField('Fecha de Fin')
    duracionEstimada = models.CharField(max_length=20)
    estado = models.CharField(max_length=40)
    usuarios = models.ManyToManyField(User, related_name='proyectos')
    def __unicode__(self):
        return self.nombre


    