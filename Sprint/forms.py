from django import forms
from django.core.context_processors import request
from django.http import request

from django.contrib.auth.models import User
from django.forms.widgets import TextInput
from django.db import models
from Sprint.models import Sprint
from django.contrib.admin import widgets


class SprintForm(forms.ModelForm):
    """
    Atributos que el usuario deber completar para la creacion
    de un nuevo pSprint
    """


    nombre=forms.CharField(widget=TextInput(attrs={'class': 'form-control'}),
                           max_length=30, help_text="Maximo 30 caracteres",label="Nombre del Sprint",)

    secuencia=forms.IntegerField(label="Nro de Secuencia",
                   widget=forms.TextInput(attrs={'class': 'form-control','type':'number','min':'0','max':'30'}))


    class Meta:
        model = Sprint
        fields = ['nombre']





class SprintFormEdit(forms.ModelForm):
    """
    Atributos que el usuario deber completar para la editar
    de un nuevo sprint
    """

    nombre=forms.CharField(widget=TextInput(attrs={'class': 'form-control','required':'required'}),
                           max_length=30, help_text="Maximo 30 caracteres",label="Nombre del Sprint",)


    class Meta:
        model = Sprint
        fields = ['nombre']

    def save(self, commit=True):
        sprint = super(SprintFormEdit, self).save(commit=True)
        # if commit:
        #    proyecto.save()
        return sprint

