from django import forms
from django.core.context_processors import request
from django.http import request

from django.contrib.auth.models import User
from django.forms.widgets import TextInput
from django.db import models
from AdminProyectos.models import Proyecto
from django.contrib.admin import widgets

class FlujoForm(forms.ModelForm):
    """
    Atributos que el usuario deber completar para la creacion
    de un nuevo proyecto
    """

    #leader=forms.CharField(widget=TextInput(attrs={'readonly':'readonly'}),required=False)
    nombre = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}),
                           max_length=30, help_text="Maximo 30 caracteres",label="Nombre del Flujo",)
    #este no estoy seguro
    #proyecto = forms.ModelChoiceField(queryset= Proyecto.objects.filter(estado='EN-ESPERA'))
    # este tampoco
    cantidad_de_actividades=forms.IntegerField(label="Numero de Actividades",help_text="Maximo 10 Actividades",
                   widget=forms.TextInput(attrs={'class': 'form-control','type':'number','min':'1','max':'10'}))
    #estado=forms.BooleanField(label="Estado")
    #coste_total=forms.IntegerField(label="Coste Total")

    class Meta:
        model = Proyecto
        fields = ['nombre','cantidad_de_actividades']
