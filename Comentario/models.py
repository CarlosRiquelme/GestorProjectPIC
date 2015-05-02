from django.db import models
from UserStory.models import UserStory
from AdminProyectos.models import Proyecto

class Comentario(models.Model):
    """
    Modelo de Proyecto con su respectivo atributos
    """
    titulo = models.CharField(max_length=30, unique=False)
    descripcion = models.CharField(max_length=120,null=True)
    userstory=models.ForeignKey(UserStory,unique=False, null=True)
    fecha_creacion= models.DateTimeField(auto_now=True)
    adjunto=models.FileField(upload_to='documents',null=True)
    porcentaje=models.IntegerField(null=True)
    hora_trabajada=models.IntegerField(null=True)

    def __unicode__(self):
        return self.titulo
