# from django.test import TestCase
# from Comentario.models import Comentario
#
#
#
# # Create your tests here.
#
# class TestComentario(TestCase):
# 	def setUp(self):
# 		print "\n TEST Comentario Existe"
# 		print "\nBuscar Comentario Creado"
# 		#Comentario.objects.create(nombre='Comentario')
# 		dato={'nombre':'flujo1', 'descripcion':'p1', 'fechaCreacion':'2015-04-09', 'userstory':'2', 'porcentaje':'ok', 'hora_trabajada':'ok'}
# 	def test_traet(self):
# 		valido=True
# 		#valido=Comentario.objects.filter(nombre='Comentario').exists()
# 		if valido==False:
# 			print "\nNo existe el Comentario"
# 		if valido == True:
# 			print "\nExiste el Comentario"
#
#
# class TestComentarioNO(TestCase):
#
# 	def setUp(self):
# 		print "\n TEST Comentario no Existe"
# 		print "\nBuscar Comentario Creado"
# 		#Comentario.objects.create(nombre='Comentario')
# 		dato={'nombre':'flujo1', 'descripcion':'p1', 'fechaCreacion':'2015-04-09', 'userstory':'2', 'porcentaje':'ok', 'hora_trabajada':'ok'}
# 	def test_traet(self):
# 		valido=False
# 		#valido=Comentario.objects.filter(nombre='Comentario').exists()
# 		if valido==False:
# 			print "\nNo existe el Comentario"
# 		if valido == True:
# 			print "\nExiste el Comentario"
