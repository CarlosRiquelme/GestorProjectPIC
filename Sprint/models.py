from django.db import models
from Flujo.models import Flujo

SPRINT_ESTADOS = (
    ('ABIERTO', 'ABIERTO'),
    ('CERRADO', 'CERRADO'),
)


class Sprint(models.Model):
    nombre = models.CharField(max_length=30, unique=True)
    fecha_creacion= models.DateTimeField(auto_now=True)
    fechaInicio = models.DateField('Fecha de Inicio')
    fechaFin = models.DateField('Fecha de Fin')
    tiempo_acumulado = models.IntegerField(null=True,default=0)
    flujo=models.ForeignKey(Flujo, null=True)
    estado=models.CharField(choices=SPRINT_ESTADOS,default='ABIERTO',max_length=30)

    def __unicode__(self):
        return self.nombre