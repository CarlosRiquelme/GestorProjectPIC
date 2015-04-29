from django.db import models
from AdminProyectos.models import Proyecto
# Create your models here.
class Flujo(models.Model):
    nombre = models.CharField(max_length=30, unique=True)
    proyecto = models.ForeignKey(Proyecto, null=True)
    cantidad_de_actividades = models.IntegerField()
    fecha_creacion= models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.nombre