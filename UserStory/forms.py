from django import forms
from django.core.context_processors import request
from django.http import request

from django.contrib.auth.models import User
from django.forms.widgets import TextInput
from django.db import models
from AdminProyectos.models import Proyecto
from UserStory.models import UserStory
from Sprint.models import Sprint
from Actividades.models import Actividad
from django.contrib.admin import widgets


class UserStoryForm(forms.ModelForm):
    """
    Atributos que el usuario deber completar para la creacion
    de un nuevo UserStory
    """
    US_PRIORIDAD = (
    ('BAJA', 'BAJA'),
    ('MEDIA', 'MEDIA'),
    ('ALTA', 'ALTA'),
)

    nombre=forms.CharField(widget=TextInput(attrs={'class': 'form-control'}),
                           max_length=30, help_text="Maximo 30 caracteres",label="Nombre del User Story",)
    descripcion=forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','rows':'3'}),
                                help_text="Maximo 120 caracteres",max_length=120,label="Descripcion")
    fechaInicio = forms.DateField(input_formats=['%Y-%m-%d'], widget=widgets.AdminDateWidget,
                                     required=True, help_text='* Ingrese en formato anho-mes-dia',
                                     error_messages={'required': 'Ingrese una fecha de Inicio del User Story'} )
    fechaFin = forms.DateField(input_formats=['%Y-%m-%d'], widget=widgets.AdminDateWidget,
                                     required=True, help_text='* Ingrese en formato anho-mes-dia',
                                     error_messages={'required': 'Ingrese una fecha de Finalizacion del User Story'} )
    #prioridad=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','rows':'3'}),
    #                            help_text="Maximo 30 caracteres",max_length=10,label="Prioridad")
    prioridad=forms.MultipleChoiceField(required=False,widget=forms.CheckboxSelectMultiple, choices=US_PRIORIDAD)
    tiempo_trabajado = forms.IntegerField(label="Tiempo Trabajado(hs)")
    porcentaje = forms.IntegerField(label="Porcentaje(%)")
    tiempo_estimado = forms.IntegerField(label="Tiempo Estimado(hs)",
                   widget=forms.TextInput(attrs={'class': 'form-control','type':'number','min':'0','max':'100'}))



    class Meta:
        model = UserStory
        fields = ['nombre','descripcion','fechaInicio','fechaFin','prioridad','tiempo_trabajado','porcentaje','tiempo_estimado']
        





class UserStoryFormEdit(forms.ModelForm):
    """
    Atributos que el usuario deber completar para la creacion
    de un nuevo UserStory
    """


    nombre=forms.CharField(widget=TextInput(attrs={'class': 'form-control','required':'required'}),
                           max_length=30, help_text="Maximo 30 caracteres",label="Nombre del UserStory",)
    
    descripcion=forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','rows':'3','required':'required'}),
                                help_text="Maximo 120 caracteres",max_length=300,label="Descripcion")


    class Meta:
        model = UserStory
        fields = ['nombre','descripcion']

    def save(self, commit=True):
        userstory = super(UserStoryFormEdit, self).save(commit=True)
        # if commit:
        #    proyecto.save()
        return userstory
