from django.db import models

# Create your models here.
#commit de prueba de divague

class Proyecto(models.Model):
    nombre = models.CharField(max_length=60)
    descripcion = models.CharField(max_length=120)
    fechaCreacion = models.DateTimeField()
    fechaInicio = models.DateTimeField('date published')
    fechaFin = models.DateTimeField()
    duracionEstimada = models.CharField(max_length=20)
    estado = models.CharField(max_length=40)
    usuarios = models.ManyToManyField(User, related_name='proyectos')
    def __unicode__(self):
        return self.nombre