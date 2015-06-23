from django.db import models
from django.contrib.auth.models import User
PROYECTOS_ESTADOS = (
    ('EN-ESPERA', 'EN-ESPERA'),
    ('EN-DESARROLLO', 'EN-DESARROLLO'),
    ('FINALIZADO', 'FINALIZADO'),
    ('CANCELADO','CANCELADO'),
    ('REVISAR', 'REVISAR'),
)
   

class Proyecto(models.Model):
    """
    Modelo de Proyecto con su respectivo atributos
    """
    nombre = models.CharField(max_length=30, unique=True, null=True)
    descripcion = models.CharField(max_length=120,null=True)
    scrumMaster=models.ForeignKey(User,unique=False, null=True)
    fecha_creacion= models.DateTimeField(auto_now=True)
    fechaInicio = models.DateField('Fecha de Inicio',null=True)
    fechaFin = models.DateField('Fecha de Fin',null=True)
    estado=models.CharField(choices=PROYECTOS_ESTADOS,default='EN-ESPERA',max_length=30)

    def __unicode__(self):
        return self.nombre
