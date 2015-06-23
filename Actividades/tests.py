from django.test import TestCase
from Actividades.models import Actividad

# Create your tests here.

class TestActividad(TestCase):
	def setUp(self):
		print "\n TEST Actividad Existe"
		print "\nBuscar Actividad Creado"
		#Actividad.objects.create(nombre='Actividad')
		dato={'nombre':'Actividad',  'fechaCreacion':'2015-04-09', 'fechaInicio':'2015-04-09','fechaFin':'2015-04-09','secuencia':'2', 'estado':'ok'}
	def test_traet(self):
		valido=True
		#valido=Flujo.objects.filter(nombre='flujo1').exists()
		if valido==False:
			print "\nNo existe la Actividad"
		if valido == True:
			print "\nExiste la Actividad"


class TestActividadNO(TestCase):

	def setUp(self):
		print "\n TEST Actividad no Existe"
		print "\nBuscar Actividad Creada"
		#Actividad.objects.create(nombre='Actividad')
		dato={'nombre':'Actividad1', 'fechaCreacion':'2015-04-09', 'fechaInicio':'2015-04-09','fechaFin':'2015-04-09','secuencia':'2', 'estado':'ok'}
	def test_traet(self):
		valido=False
		#valido=Flujo.objects.filter(nombre='flujo23').exists()
		if valido==False:
			print "\nNo existe la Actividad"
		if valido == True:
			print "\nExiste la Actividad"


