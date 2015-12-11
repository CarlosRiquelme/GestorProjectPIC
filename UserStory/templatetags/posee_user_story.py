from django.contrib.sites.models import Site
from django import template
from UserStory.models import UserStory

register = template.Library()

@register.simple_tag
def posee_us(id_proyecto,id_user):
    us=UserStory.objects.filter(proyecto_id=id_proyecto,usuario_id=id_user)
    if us.exists():
        return '<button type="button" class="btn btn-primary disabled ">Desasignar</button>'
    else:
        return '<button type="button" class="btn btn-primary ">Desasignar</button>'
