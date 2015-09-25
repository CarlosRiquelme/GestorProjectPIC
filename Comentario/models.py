from django.db import models
from UserStory.models import UserStory
from AdminProyectos.models import Proyecto

def url(self):
    ruta="/media/documento"
    return ruta

class Comentario(models.Model):
    """
    Modelo de Proyecto con su respectivo atributos
    """

    titulo = models.CharField(max_length=30, unique=False)
    descripcion = models.CharField(max_length=120,null=True)
    userstory=models.ForeignKey(UserStory,unique=False, null=True)
    fecha_creacion= models.DateTimeField(auto_now=True)
    porcentaje_actividad=models.IntegerField(null=True)
    hora_trabajada=models.IntegerField(null=True)
    porcentaje_userstory=models.FloatField(null=True)
    adjunto=models.NullBooleanField()

    def __unicode__(self):
        return self.titulo

    def get_archivo(self):

        docs=Document.objects.filter(comentario=self)
        if docs.count()>0:
            return docs[0].docfile
        else:
            return None

    def get_archivo_id(self):

        docs=Document.objects.filter(comentario=self)
        if docs.count()>0:
            return docs[0].id
        else:
            return None


from db_file_storage.model_utils import delete_file, delete_file_if_needed

class Document(models.Model):
    comentario=models.ForeignKey(Comentario)
    docfile = models.FileField(
        upload_to='Comentario.Archivo/bytes/filename/mimetype',
        blank=True,
        null=True
    )

    def get_absolute_url(self):
        return reverse('Document.edit', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        delete_file_if_needed(self, 'docfile')
        super(Document, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super(Document, self).delete(*args, **kwargs)
        delete_file(self, 'docfile')


class Archivo(models.Model):
    bytes = models.TextField()
    filename = models.CharField(max_length=255)
    mimetype = models.CharField(max_length=50)

    def __unicode__(self):
        return self.filename
