from django import forms
from django.core.context_processors import request
from django.http import request

from django.contrib.auth.models import User
from django.forms.widgets import TextInput
from django.db import models
from Actividades.models import Actividad
from Flujo.models import Flujo
from django.contrib.admin import widgets


class ActividadForm(forms.ModelForm):
    """
    Atributos que el usuario deber completar para la creacion
    de un nuevo proyecto
    """

    #leader=forms.CharField(widget=TextInput(attrs={'readonly':'readonly'}),required=False)
    nombre=forms.CharField(widget=TextInput(attrs={'class': 'form-control'}),
                           max_length=30, help_text="Maximo 30 caracteres",label="Nombre de la Actividad",)
    fechaInicio = forms.DateField(input_formats=['%Y-%m-%d'], widget=widgets.AdminDateWidget,
                                     required=True, help_text='* Ingrese en formato anho-mes-dia',
                                     error_messages={'required': 'Ingrese una fecha de Inicio del proyecto'} )
    fechaFin = forms.DateField(input_formats=['%Y-%m-%d'], widget=widgets.AdminDateWidget,
                                     required=True, help_text='* Ingrese en formato anho-mes-dia',
                                     error_messages={'required': 'Ingrese una fecha de Finalizacion del proyecto'} )
    secuencia=forms.IntegerField(label="Numero de la  Actividad",help_text="Maximo 10 Actividades",
                   widget=forms.TextInput(attrs={'class': 'form-control','type':'number','min':'1','max':'10'}))

    class Meta:
        model = Actividad
        fields = ['nombre','fechaInicio','fechaFin','secuencia']


    def save(self, commit=True):
        actividad = super(ActividadForm, self).save(commit=False)
        if commit:
            actividad.save()
        return actividad



