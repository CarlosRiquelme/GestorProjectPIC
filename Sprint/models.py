from django.db import models
from AdminProyectos.models import Proyecto
SPRINT_ESTADOS = (
    ('EN-ESPERA', 'EN-ESPERA'),
    ('ABIERTO', 'ABIERTO'),
    ('CERRADO', 'CERRADO'),
)


class Sprint(models.Model):
    nombre = models.CharField(max_length=30, unique=True)
    fecha_creacion= models.DateTimeField(auto_now=True)
    fechaInicio=models.DateField(null=True)
    fechaInicio=models.DateField(null=True)
    tiempo_acumulado = models.IntegerField(null=True,default=0)
    proyecto=models.ForeignKey(Proyecto, null=True)
    estado=models.CharField(choices=SPRINT_ESTADOS,default='ABIERTO',max_length=30)
    secuencia=models.IntegerField()

    def __unicode__(self):
        return self.nombre


class Estimacion_Proyecto(models.Model):
    proyecto=models.ForeignKey(Proyecto)
    fechaInicio=models.DateField(null=True)
    fechaFin=models.DateField(null=True)



class Estimacion_Sprint(models.Model):
    sprint=models.ForeignKey(Sprint)
    fechaInicio=models.DateField(null=True)
    fechaFin=models.DateField(null=True)
    duracion=models.IntegerField()
    proyecto_estimacion=models.ForeignKey(Estimacion_Proyecto)