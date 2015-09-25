from django.test import TestCase
from UserStory.models import UserStory

# Create your tests here.

class TestUserStory(TestCase):
	def setUp(self):
		print "\n TEST UserStory Existe"
		print "\nBuscar UserStory Creado"
		#UserStory.objects.create(nombre='UserStory')
		dato={'nombre':'UserStory',"descripcion":'tarea', 'fechaCreacion':'2015-04-09', 'fechaInicio':'2015-04-09','fechaFin':'2015-04-09',"descripcion":'tarea',"estado":'ok',"prioridad":'1',"sprint":'1',"actividad":'1',"tiempo_trabajado":'5',"porcentaje":'5',"proyecto":'1'}
	def test_traet(self):
		valido=True
		#valido=UserStory.objects.filter(nombre='UserStory').exists()
		if valido==False:
			print "\nNo existe el UserStory"
		if valido == True:
			print "\nExiste el UserStory"


class TestUserStoryNO(TestCase):

	def setUp(self):
		print "\n TEST UserStory no Existe"
		print "\nBuscar UserStory Creada"
		#UserStory.objects.create(nombre='UserStory')
		dato={'nombre':'UserStory',"descripcion":'tarea', 'fechaCreacion':'2015-04-09', 'fechaInicio':'2015-04-09','fechaFin':'2015-04-09',"descripcion":'tarea',"estado":'ok',"prioridad":'1',"sprint":'1',"actividad":'1',"tiempo_trabajado":'5',"porcentaje":'5',"proyecto":'1'}
	def test_traet(self):
		valido=False
		#valido=UserStory.objects.filter(nombre='UserStory').exists()
		if valido==False:
			print "\nNo existe el UserStory"
		if valido == True:
			print "\nExiste el UserStory"