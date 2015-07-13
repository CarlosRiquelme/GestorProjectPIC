from django import forms
from django.forms import ModelForm
from django.core.context_processors import request
from django.http import request

from django.contrib.auth.models import User
from django.forms.widgets import TextInput, FileInput
from Comentario.models import Comentario, Document
from django.db import models
from AdminProyectos.models import Proyecto
from UserStory.models import UserStory
from django.contrib.admin import widgets

class ComentarioForm(forms.ModelForm):
    """
    Atributos que el usuario deber completar para la creacion
    de un nuevo proyecto
    """


    titulo = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}),
                           max_length=30, help_text="Maximo 30 caracteres",label="Titulo",)

    descripcion = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','rows':'3'}),
                                help_text="Maximo 120 caracteres",max_length=120,label="Descripcion")

    hora_trabajada=forms.IntegerField(label="Hora Trabajada",
                   widget=forms.TextInput(attrs={'class': 'form-control','type':'number','min':'1','max':'16'}))

    class Meta:
        model = Comentario
        fields = ['titulo','descripcion','hora_trabajada']



#
#
# class DocumentForm(forms.ModelForm):
#     class Meta:
#         model = Document
#         exclude = ['comentario']
#
#


#.models import Console
from db_file_storage.form_widgets import DBClearableFileInput
from django import forms

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        exclude = []
        widgets = {
            'docfile': DBClearableFileInput
        }