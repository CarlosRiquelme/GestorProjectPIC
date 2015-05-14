from django import forms
from django.core.context_processors import request
from django.http import request

from django.contrib.auth.models import User
from django.forms.widgets import TextInput
from django.db import models
from AdminProyectos.models import Proyecto
from django.contrib.admin import widgets


class ProyectoForm(forms.ModelForm):
    """
    Atributos que el usuario deber completar para la creacion
    de un nuevo proyecto
    """

    #leader=forms.CharField(widget=TextInput(attrs={'readonly':'readonly'}),required=False)
    nombre=forms.CharField(widget=TextInput(attrs={'class': 'form-control'}),
                           max_length=30, help_text="Maximo 30 caracteres",label="Nombre del Proyecto",)
    descripcion=forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','rows':'3'}),
                                help_text="Maximo 120 caracteres",max_length=120,label="Descripcion")
    scrumMaster=forms.ModelChoiceField(queryset= User.objects.filter(is_active=True))
    fechaInicio = forms.DateField(input_formats=['%Y-%m-%d'], widget=widgets.AdminDateWidget,
                                     required=True, help_text='* Ingrese en formato anho-mes-dia',
                                     error_messages={'required': 'Ingrese una fecha de Inicio del proyecto'} )
    fechaFin = forms.DateField(input_formats=['%Y-%m-%d'], widget=widgets.AdminDateWidget,
                                     required=True, help_text='* Ingrese en formato anho-mes-dia',
                                     error_messages={'required': 'Ingrese una fecha de Finalizacion del proyecto'} )
    #rol_usuario = models.ManyToManyField(Usuario_Rol, related_name='proyectos')

    class Meta:
        model = Proyecto
        fields = ['nombre','descripcion','scrumMaster','fechaInicio','fechaFin']

    def clean(self):
        cleaned_data = super(ProyectoForm, self).clean()
        fechaFin= cleaned_data.get("fechaFin")
        fechaInicio=cleaned_data.get("fechaInicio")
        if fechaFin <= fechaInicio:
            raise forms.ValidationError("La Fecha de Finalizacion no puede ser Menor que la de Inicio")


    def save(self, commit=True):
        proyecto = super(ProyectoForm, self).save(commit=False)
        if commit:
            proyecto.save()
        return proyecto



class ProyectoFormEdit(forms.ModelForm):
    """
    Atributos que el usuario deber completar para la creacion
    de un nuevo proyecto
    """

    nombre=forms.CharField(widget=TextInput(attrs={'class': 'form-control','required':'required'}),
                           max_length=30, help_text="Maximo 30 caracteres",label="Nombre del Proyecto",)
    
    descripcion=forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','rows':'3','required':'required'}),
                                help_text="Maximo 120 caracteres",max_length=300,label="Descripcion")
    class Meta:
        model = Proyecto
        fields = ['nombre','descripcion']

    def save(self, commit=True):
        proyecto = super(ProyectoFormEdit, self).save(commit=True)
        return proyecto
