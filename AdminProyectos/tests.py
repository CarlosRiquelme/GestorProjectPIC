# from django.test import TestCase
# from AdminProyectos.models import Proyecto
# from django.contrib.auth.models import User, Group
# from django.test import Client
# # Create your tests here.
#
# class TestLista(TestCase):
#
#
#     def test_listaProyecto(self):
#         proyecto=Proyecto.objects.create(nombre='PROYECTO1',descripcion='hola', fecha_creacion='2015-05-15 21:03:31-04',
#                                          fechaInicio='2015-05-16',fechaFin='2015-06-16', estado='EN-ESPERA')
#         #usuario=User.objects.create(username='admin',password='admin')
#         usuario=Client()
#         resp=usuario.get('/proyectos/')
#         self.assertEqual(resp.status_code, 200)
#         print "\n Lista Proyecto "
#
#
#
#
# class TestProyecto(TestCase):
# 	def setUp(self):
# 		print "\n TEST Proyecto Existe"
# 		print "\nBuscar Proyecto Creado"
# 		#Proyecto.objects.create(nombre='Proyecto')
# 		dato={'nombre':'project1', 'descripcion':'p1', 'fechaCreacion':'2015-04-09 21:03:31-04', 'fechaInicio':'2015-04-09 21:03:31-04', 'fechaFin':'2015-04-09 21:03:31-04', 'duracionEstimada':'3', 'estado':'ok', 'usuarios':'1'}
# 	def test_traet(self):
# 		valido=True
# 		#valido=Proyecto.objects.filter(nombre='Proyecto').exists()
# 		if valido==False:
# 			print "\nNo existe el Proyecto"
# 		if valido == True:
# 			print "\nExiste el Proyecto"
#
#
# class TestProyectoNO(TestCase):
#
# 	def setUp(self):
# 		print "\n TEST Proyecto no Existe"
# 		print "\nBuscar Proyecto Creada"
# 		#UserStory.objects.create(nombre='Proyecto')
# 		dato={'nombre':'project1', 'descripcion':'p1', 'fechaCreacion':'2015-04-09 21:03:31-04', 'fechaInicio':'2015-04-09 21:03:31-04', 'fechaFin':'2015-04-09 21:03:31-04', 'duracionEstimada':'3', 'estado':'ok', 'usuarios':'1'}
# 	def test_traet(self):
# 		valido=False
# 		#valido=Proyecto.objects.filter(nombre='Proyecto').exists()
# 		if valido==False:
# 			print "\nNo existe el Proyecto"
# 		if valido == True:
# 			print "\nExiste el Proyecto"