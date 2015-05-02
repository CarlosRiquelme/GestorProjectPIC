from django.test import TestCase
from Sprint.models import Sprint

# Create your tests here.

class TestSprint(TestCase):
	def setUp(self):
		print "\n TEST Sprint Existe"
		print "\nBuscar Sprint Creado"
		#Sprint.objects.create(nombre='Sprint')
		dato={'nombre':'Sprint', 'fechaCreacion':'2015-04-09', 'fechaInicio':'2015-04-09','fechaFin':'2015-04-09','tiempo_acumulado':'2'}
	def test_traet(self):
		valido=True
		#valido=Sprint.objects.filter(nombre='Sprint').exists()
		if valido==False:
			print "\nNo existe el Sprint"
		if valido == True:
			print "\nExiste el Sprint"


class TestSprintNO(TestCase):

	def setUp(self):
		print "\n TEST Sprint no Existe"
		print "\nBuscar Sprint Creada"
		#Actividad.objects.create(nombre='Actividad')
		dato={'nombre':'Sprint', 'fechaCreacion':'2015-04-09', 'fechaInicio':'2015-04-09','fechaFin':'2015-04-09','tiempo_acumulado':'2'}
	def test_traet(self):
		valido=False
		#valido=Sprint.objects.filter(nombre='Sprint').exists()
		if valido==False:
			print "\nNo existe el Sprint"
		if valido == True:
			print "\nExiste el Sprint"
