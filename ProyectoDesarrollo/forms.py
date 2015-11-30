from UserStory.models import UserStory
from django import forms


class UserStoryFormTiempo(forms.ModelForm):




    tiempo_estimado = forms.IntegerField(label="Nuevo Tiempo Estimado(hs)",
                   widget=forms.TextInput(attrs={'class': 'form-control','type':'number','min':'1','max':'48'}),
                   help_text="Debe aumentar las horas de Estimacion del User Story")



    class Meta:
        model = UserStory
        fields = ['tiempo_estimado']
