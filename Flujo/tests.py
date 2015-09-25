from django.test import TestCase
from Flujo.models import Flujo

# Create your tests here.

class TestFlujo(TestCase):
	def setUp(self):
		print "\n TEST Flujo Existe"
		print "\nBuscar Flujo Creado"
		#Flujo.objects.create(nombre='flujo1')
		dato={'nombre':'flujo1', 'proyecto':'p1', 'fechaCreacion':'2015-04-09', 'cantidad_de_actividades':'2', 'estado':'ok'}
	def test_traet(self):
		valido=True
		#valido=Flujo.objects.filter(nombre='flujo1').exists()
		if valido==False:
			print "\nNo existe el Flujo"
		if valido == True:
			print "\nExiste el Flujo"


class TestFlujoNO(TestCase):

	def setUp(self):
		print "\n TEST Flujo no Existe"
		print "\nBuscar Flujo Creado"
		#Flujo.objects.create(nombre='flujo1')
		dato={'nombre':'flujo1', 'proyecto':'p1', 'fechaCreacion':'2015-04-09', 'cantidad_de_actividades':'2', 'estado':'ok'}
	def test_traet(self):
		valido=False
		#valido=Flujo.objects.filter(nombre='flujo23').exists()
		if valido==False:
			print "\nNo existe el Flujo"
		if valido == True:
			print "\nExiste el Flujo"

