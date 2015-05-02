from django.db import models
from AdminProyectos.models import Proyecto
# Create your models here.

FLUJO_ESTADOS = (
    ('NO-CREADO', 'NO-CREADO'),
    ('CREADO', 'CREADO'),
)


class Flujo(models.Model):
    nombre = models.CharField(max_length=30, unique=True)
    proyecto = models.ForeignKey(Proyecto, null=True)
    cantidad_de_actividades = models.IntegerField()
    fecha_creacion= models.DateTimeField(auto_now=True)
    estado=models.CharField(choices=FLUJO_ESTADOS,default='NO-CREADO',max_length=30)

    def __unicode__(self):
        return self.nombre