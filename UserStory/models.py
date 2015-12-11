from django.db import models
from Sprint.models import Sprint
from Actividades.models import Actividad
from AdminProyectos.models import Proyecto
from django.contrib.auth.models import User
# Create your models here.
US_ESTADOS = (
    ('CREADO', 'CREADO'),
    ('TODO', 'TODO'),
    ('DOING', 'DOING'),
    ('DONE', 'DONE'),
    ('REASIGNAR_SPRINT', 'REASIGNAR_SPRINT'),
    ('REASIGNAR_ACTIVIDAD', 'REASIGNAR_ACTIVIDAD'),
    ('FINALIZADO', 'FINALIZADO'),
    ('CANCELADO', 'CANCELADO'),
    ('REVISAR_TIEMPO','REVISAR_TIEMPO'),
    ('REVISAR','REVISAR'),
    ('REVISAR_E','REVISAR_E'),
    ('REVISAR_FIN_AC','REVISAR_FIN_AC'),
    ('REVISAR_FIN','REVISAR_FIN'),

)
US_PRIORIDAD = (
    ('BAJA', 'B'),
    ('MEDIA', 'M'),
    ('ALTA', 'A'),
    ('SUPER-ALTA', 'SUPER-ALTA'),
)

class UserStory(models.Model):
    nombre = models.CharField(max_length=30, unique=False)
    descripcion = models.CharField(max_length=150)
    fecha_creacion= models.DateTimeField(auto_now=True)
    estado=models.CharField(choices=US_ESTADOS,default='CREADO',max_length=30)
    prioridad=models.CharField(max_length=30)
    sprint=models.ForeignKey(Sprint, unique=False, null=True)
    actividad=models.ForeignKey(Actividad, unique=False, null=True)
    tiempo_trabajado = models.IntegerField(null=True)
    suma_trabajadas=models.IntegerField(null=True, default=0)
    porcentaje = models.FloatField(null=True)
    proyecto=models.ForeignKey(Proyecto, null=True)
    tiempo_estimado=models.IntegerField(null=True,default=0)
    usuario=models.ForeignKey(User, null=True)
    nro_sprint=models.IntegerField(null=True)
    nro_actividad=models.IntegerField(null=True)
    porcentaje_actividad=models.FloatField(null=True)
    tiempo_demas=models.IntegerField(null=True, default=0)


    def __unicode__(self):
        return self.nombre

class UserStory_aux(models.Model):
    nombre = models.CharField(max_length=30, unique=False)
    descripcion = models.CharField(max_length=150)
    fecha_creacion= models.DateTimeField(auto_now=True)
    estado=models.CharField(choices=US_ESTADOS,default='CREADO',max_length=30)
    prioridad=models.CharField(max_length=30)
    sprint=models.ForeignKey(Sprint, unique=False, null=True)
    actividad=models.ForeignKey(Actividad, unique=False, null=True)
    tiempo_trabajado = models.IntegerField(null=True)
    suma_trabajadas=models.IntegerField(null=True, default=0)
    porcentaje = models.FloatField(null=True)
    proyecto=models.ForeignKey(Proyecto, null=True)
    tiempo_estimado=models.IntegerField(null=True,default=0)
    usuario=models.ForeignKey(User, null=True)
    nro_sprint=models.IntegerField(null=True)
    nro_actividad=models.IntegerField(null=True)
    porcentaje_actividad=models.FloatField(null=True)


    def __unicode__(self):
        return self.nombre

class US_Estado_ultimo(models.Model):
    us=models.ForeignKey(UserStory)
    estado=models.CharField(max_length=30)
    estado_actual=models.CharField(max_length=30)


class Historial_US(models.Model):
    us=models.ForeignKey(UserStory, null=True)
    nombre_us=models.CharField(max_length=100, null=True)
    descripcion=models.CharField(max_length=200)
    fecha=models.DateTimeField(auto_now=True)
    proyecto=models.ForeignKey(Proyecto)

class UserStory_Sprint(models.Model):
    us=models.ForeignKey(UserStory, null=True)
    sprint=models.ForeignKey(Sprint)
    horas_trabajadas=models.IntegerField(default=0)
    horas_estimada=models.IntegerField(default=0)
    proyecto=models.ForeignKey(Proyecto)
    fecha=models.DateField(null=True)