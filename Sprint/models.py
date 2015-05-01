from django.db import models


# Create your models here.
class Sprint(models.Model):
    nombre = models.CharField(max_length=30, unique=True)
    fecha_creacion= models.DateTimeField(auto_now=True)
    fechaInicio = models.DateField('Fecha de Inicio')
    fechaFin = models.DateField('Fecha de Fin')
    tiempo_acumulado = models.IntegerField(null=True)

    def __unicode__(self):
        return self.nombre