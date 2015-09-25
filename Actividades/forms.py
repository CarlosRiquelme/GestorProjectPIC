from django import forms
from django.core.context_processors import request
from django.http import request

from django.contrib.auth.models import User
from django.forms.widgets import TextInput
from django.db import models
from Actividades.models import Actividad
from django.contrib.admin import widgets


class ActividadForm(forms.ModelForm):
    """
    Atributos que el usuario deber completar para la creacion
    de un nuevo proyecto
    """

    #leader=forms.CharField(widget=TextInput(attrs={'readonly':'readonly'}),required=False)
    nombre=forms.CharField(widget=TextInput(attrs={'class': 'form-control'}),
                           max_length=30, help_text="Maximo 30 caracteres",label="Nombre de la Actividad",)


    class Meta:
        model = Actividad
        fields = ['nombre']


    def save(self, commit=True):
        actividad = super(ActividadForm, self).save(commit=False)
        if commit:
            actividad.save()
        return actividad


class EditActividadForm(forms.ModelForm):
    nombre=forms.CharField(widget=TextInput(attrs={'class':'form-control'}), label="nombre")

    class Meta:
        model = Actividad
        fields = ['nombre']

    def save(self, commit=True):
        actividad = super(ActividadForm, self).save(commit=False)
        if commit:
            actividad.save()
        return actividad
