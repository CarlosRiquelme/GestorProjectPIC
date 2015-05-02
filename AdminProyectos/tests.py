from django.test import TestCase
from AdminProyectos.models import Proyecto

# Create your tests here.

class TestProyecto(TestCase):
	def setUp(self):
		print "\n TEST Proyecto Existe"
		print "\nBuscar Proyecto Creado"
		#Proyecto.objects.create(nombre='Proyecto')
		dato={'nombre':'project1', 'descripcion':'p1', 'fechaCreacion':'2015-04-09 21:03:31-04', 'fechaInicio':'2015-04-09 21:03:31-04', 'fechaFin':'2015-04-09 21:03:31-04', 'duracionEstimada':'3', 'estado':'ok', 'usuarios':'1'}
	def test_traet(self):
		valido=True
		#valido=Proyecto.objects.filter(nombre='Proyecto').exists()
		if valido==False:
			print "\nNo existe el Proyecto"
		if valido == True:
			print "\nExiste el Proyecto"


class TestProyectoNO(TestCase):

	def setUp(self):
		print "\n TEST Proyecto no Existe"
		print "\nBuscar Proyecto Creada"
		#UserStory.objects.create(nombre='Proyecto')
		dato={'nombre':'project1', 'descripcion':'p1', 'fechaCreacion':'2015-04-09 21:03:31-04', 'fechaInicio':'2015-04-09 21:03:31-04', 'fechaFin':'2015-04-09 21:03:31-04', 'duracionEstimada':'3', 'estado':'ok', 'usuarios':'1'}
	def test_traet(self):
		valido=False
		#valido=Proyecto.objects.filter(nombre='Proyecto').exists()
		if valido==False:
			print "\nNo existe el Proyecto"
		if valido == True:
			print "\nExiste el Proyecto"