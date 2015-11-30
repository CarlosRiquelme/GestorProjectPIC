from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from Sprint.models import Sprint
from AdminProyectos.models import Proyecto
from AdminProyectos.forms import ProyectoForm
from django.utils import timezone
from django.core.urlresolvers import reverse

class TestProyecto(TestCase):

    user=User.objects.get(username='marcial_sm')

    def proyecto_create(self, nombre='proyecto_test',descripcion='p_test',fechaInicio='2015-11-11',estado='EN-ESPERA',scrumMaster=user):
        return Proyecto.objects.create(nombre=nombre,descripcion=descripcion,fechaInicio=fechaInicio,estado=estado,scrumMaster=scrumMaster)

    def test_create_model(self):
        print '\n'
        print "Test del Model de Proyecto"
        p=self.proyecto_create()
        self.assertTrue(isinstance(p, Proyecto))
        self.assertEqual(p.__unicode__(), p.nombre)

    def test_proyecto_list_view(self):
        print '\n'
        print "Test del Views de Proyecto"
        p=self.proyecto_create()
        url = reverse("AdminProyectos.views.nuevo_proyecto")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)


    def test_proyecto_form(self):
        c=Client()
        #User.objects.create(username='user_test', password='123')
        print "----------Prueba de Creacion de Proyecto----------------"

        resp=c.post('/proyecto/nuevo',{'nombre':'proyecto_test','descripcion':'p test',
                                   'fechaInicio':'2015-11-25','estado':'EN-ESPERA',
                                   'scrumMaster':'2'})
        self.assertEqual(resp.status_code,302)
        print "Se pudo crear el status_code arrojo:  "+str(resp.status_code)
        print "\n"


class TestSprint(TestCase):
    def test_sprint(self):
        c=Client()
        #User.objects.create(username='user_test', password='123')
        print "\n"
        print "----------Prueba de Creacion de Sprint----------------"

        resp=c.post('/sprint/nuevo/10/',{'nombre':'sprint_tes','secuencia':'1'})

        self.assertEqual(resp.status_code,302)
    def test_sprint_nuevo(self):
        c=Client()
        sprint=Sprint()
        sprint.nombre='sprint_test'
        sprint.secuencia='1'
        resp=c.post('/sprint/nuevo/10/',{'nombre':'sprint_tes','secuencia':'1'})
        print resp.status_code


class TestActividad(TestCase):
    def test_actividad_create(self):
        c=Client()
        #User.objects.create(username='user_test', password='123')
        print "\n"
        print "----------Prueba de Creacion de Actividad----------------"

        resp=c.post('/actividad/nueva/10/',{'nombre':'actividad_tes','secuencia':'1'})

        self.assertEqual(resp.status_code,302)

