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


    fechaInicio = forms.DateField(input_formats=['%Y-%m-%d'], widget=widgets.AdminDateWidget,
                                     required=True, help_text='* Ingrese en formato anho-mes-dia',
                                     error_messages={'required': 'Ingrese una fecha de Inicio del Sprint'} )

    fechaFin = forms.DateField(input_formats=['%Y-%m-%d'], widget=widgets.AdminDateWidget,
                                     required=True, help_text='* Ingrese en formato anho-mes-dia',
                                     error_messages={'required': 'Ingrese una fecha de Finalizacion del Sprint'} )

    tiempo_acumulado =  forms.IntegerField(label="Tiempo Acumulado(hs)",
                   widget=forms.TextInput(attrs={'class': 'form-control','type':'number','min':'0','max':'100'}))


    class Meta:
        model = Sprint
        fields = ['nombre','fechaInicio','fechaFin','tiempo_acumulado']




class SprintFormEdit(forms.ModelForm):
    """
    Atributos que el usuario deber completar para la editar
    de un nuevo sprint
    """

    #leader=forms.CharField(widget=TextInput(attrs={'readonly':'readonly'}),required=False)
    nombre=forms.CharField(widget=TextInput(attrs={'class': 'form-control','required':'required'}),
                           max_length=30, help_text="Maximo 30 caracteres",label="Nombre del Sprint",)

    #leader=forms.ModelChoiceField(queryset=User.objects.all())
    #fecha_creacion=forms.DateTimeField()
    # complejidad=forms.IntegerField(label="Complejidad")

    #estado=forms.BooleanField(label="Estado")
    #coste_total=forms.IntegerField(label="Coste Total")

    class Meta:
        model = Sprint
        fields = ['nombre']

    def save(self, commit=True):
        sprint = super(SprintFormEdit, self).save(commit=True)
        # if commit:
        #    proyecto.save()
        return sprint

