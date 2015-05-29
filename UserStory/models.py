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
)
US_PRIORIDAD = (
    ('BAJA', 'BAJA'),
    ('MEDIA', 'MEDIA'),
    ('ALTA', 'ALTA'),
    ('SUPER-ALTA', 'SUPER-ALTA'),
)

class UserStory(models.Model):
    nombre = models.CharField(max_length=30, unique=True)
    descripcion = models.CharField(max_length=150)
    fecha_creacion= models.DateTimeField(auto_now=True)
    estado=models.CharField(choices=US_ESTADOS,default='CREADO',max_length=30)
    prioridad=models.CharField(max_length=30)
    sprint=models.ForeignKey(Sprint, unique=False, null=True)
    actividad=models.ForeignKey(Actividad, unique=False, null=True)
    tiempo_trabajado = models.IntegerField(null=True)
    porcentaje = models.IntegerField(null=True)
    proyecto=models.ForeignKey(Proyecto, null=True)
    tiempo_estimado=models.IntegerField(null=True)
    usuario=models.ForeignKey(User, null=True)

    def __unicode__(self):
        return self.nombre