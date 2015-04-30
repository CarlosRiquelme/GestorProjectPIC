from django.db import models
from Flujo.models import Flujo

FLUJO_ESTADOS = (
    ('PROGRAMADO', 'PROGRAMADO'),
    ('INICIADO', 'INICIADO'),
    ('FINALIZADO', 'FINALIZADO'),
)


class Actividad(models.Model):
    nombre = models.CharField(max_length=30, unique=True)
    flujo=models.ForeignKey(Flujo, unique=False, null=True)
    fecha_creacion= models.DateTimeField(auto_now=True)
    fechaInicio = models.DateField('Fecha de Inicio')
    fechaFin = models.DateField('Fecha de Fin')
    estado=models.CharField(choices=FLUJO_ESTADOS,default='PROGRAMADO',max_length=30)
    secuencia=models.IntegerField(null=True)

    def __unicode__(self):
        return self.nombre