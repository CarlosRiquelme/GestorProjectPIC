from django.contrib import admin
from PIC.models import Proyecto, Flujo,Usuario_rol, User_Story, Sprint

# Register your models here.
admin.site.register(Proyecto)
admin.site.register(Flujo)
admin.site.register(Usuario_rol)
admin.site.register(Sprint)
admin.site.register(User_Story)
