from django.contrib import admin
from Comentario.forms import DocumentForm
#from Comentario.models import
from django.http import HttpResponseRedirect


from django.contrib import admin
from django.core.urlresolvers import reverse
from Comentario.models import Document


class DocumentAdmin(admin.ModelAdmin):
    form = DocumentForm


    def response_add(self, request, obj, post_url_continue=None):
        """This makes the response after adding go to another apps changelist for some model"""
        return HttpResponseRedirect(reverse("admin:otherappname_modelname_changelist"))


    def response_add(self, request, obj, post_url_continue=None):
        """This makes the response go to the newly created model's change page
        without using reverse"""
        return HttpResponseRedirect("/comentario/miscomentarios/%s"%request.GET.get("id_us"))

    def response_change(self, request, obj, post_url_continue=None):
        """This makes the response go to the newly created model's change page
        without using reverse"""
        return HttpResponseRedirect("/comentario/miscomentarios/%s"%request.GET.get("id_us"))

    def response_delete(self, request, obj, post_url_continue=None):
        """This makes the response go to the newly created model's change page
        without using reverse"""
        return HttpResponseRedirect("/comentario/miscomentarios/%s"%request.GET.get("id_us"))


admin.site.register(Document,DocumentAdmin)
