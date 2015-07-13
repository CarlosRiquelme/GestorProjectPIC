from UserStory.models import UserStory
from django import forms


class UserStoryFormTiempo(forms.ModelForm):



    tiempo_estimado = forms.IntegerField(label="Nuevo Tiempo Estimado(hs)",
                   widget=forms.TextInput(attrs={'class': 'form-control','type':'number','min':'0','max':'100'}))


    class Meta:
        model = UserStory
        fields = ['tiempo_estimado']
