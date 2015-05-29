from django.db import models
from Flujo.models import Flujo
from AdminProyectos.models import Proyecto



class Actividad(models.Model):
    nombre = models.CharField(max_length=30)
    proyecto=models.ForeignKey(Proyecto, unique=False, null=True)
    fecha_creacion= models.DateTimeField(auto_now=True)
    secuencia=models.IntegerField(null=True)

    def __unicode__(self):
        return self.nombre