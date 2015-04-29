# from datetime import datetime
# from django.utils import timezone
# from django.test import TestCase
# from django.test.utils import override_settings
# from django.contrib.auth.models import User, Group
# from PIC.models import Proyecto, Flujo
#
#
# class TestUserBD(TestCase):
# 	"""
# 		Test para ver si la Base de Datos
# 		se encuentra vacio
# 	"""
# 	def test_numero_elementos(self):
# 		print("\n TEST: Verificar si esta vacia la Base de Datos")
# 		try:
# 			self.assertEqual(0,len(User.objets.all()))
# 		except:
# 			print("Base de Datos vacia, el numero de usuarios es distintos de 0")
# 			return
# 		print("Base de Datos no se encuentra vacia")
#
# class TestLogin(TestCase):
# 	"""
#
# 	Test para prueba de login de un usuario registrado
# 	en el sistema
#
# 	"""
#
# 	def test_login_usuario(self):
# 		print("\n TEST: Loguear Usuario Registrado")
# 		#username="admin"
# 		#password="admin"
# 		User.objects.create(username="moises", password="moises")
# 		try:
# 			#vamos a la pantalla de inicio
# 			resp=self.client.get('/admin/login/?next=/admin/')
# 			self.assertEqual(resp.status_code,200)
# 			#logueamos con el usuario admin
# 			login = self.client.login(username="moises", password="moises")
# 			self.assertFalse(login)
# 		except:
# 			if resp.status_code == 404:
# 				print("Prueba Fallida, la url no existe")
# 			print("Prueba Fallida, el usuario no existe")
# 			return
# 		print("Prueba exitosa, el usuario pudo iniciar sesion")
#
# class testf(TestCase):
# 	def testf(self):
# 		print "\n"
# class testNologin(TestCase):
# 	"""
# 	Test prueba de login de un usuario no registrado
# 	en el sistema
#
# 	"""
# 	def test_login_usuario(self):
# 		print("\n TEST: Loguear Usuario NO Registrado")
# 		usuario="admin"
# 		password="admin"
# 		try:
# 			#vamos a la pantalla de inicio
# 			resp=self.client.get('/admin/login/?next=/admin/')
# 			self.assertEqual(resp.status_code,200)
# 			#logueamos con el usuario admin
# 			login = self.client.login(username=usuario, password=password)
# 			self.assertTrue(login)
# 		except:
# 			if resp.status_code == 404:
# 				print("Prueba Fallida, la url no existe")
# 			print("Prueba Exitosa, el usuario no registrado no pudo acceder")
# 			return
# 		print("Prueba Fallida, el usuario pudo iniciar sesion")
#
# class UsuarioTestCase (TestCase):
#
#   def setUp (self):
#      print "\n TEST: USUARIO"
#      print "\n ------Buscar el usuario creado"
#      User.objects.create(username="aa", password="aa")
#   def test_traer(self):
#       valido = False
#       valido = User.objects.filter(username="aa").exists()
#       if valido==True:
#           print "\n------Se ha encontrado el usuario creado"
#
#       print "\n ------Buscar un usuario inexistente"
#       valido = True
#       valido = User.objects.filter(username='"oo"').exists()
#       if valido==False:
#           print "\n------No existe el usuario buscado"
#
# class GrupoTestCase (TestCase):
#
#   def setUp (self):
#      print "\n TEST GRUPO"
#      print "\n --Buscar el Grupo creado"
#      Group.objects.create(name="aa")
#
#   def test_traer(self):
#       valido = False
#       valido = Group.objects.filter(name="aa").exists()
#       if valido==True:
#           print "\n---Se ha encontrado el Grupo creado"
#
#       print "\n --Buscar un Grupo inexistente"
#       valido = True
#       valido = Group.objects.filter(name='"oo"').exists()
#       if valido==False:
#           print "\n---No existe el grupo buscado"
# ################################################################################################
# ######TEST PROYECTO
# ################################################################################################
#
# class TestProyecto(TestCase):
#
# 	def setUp(self):
# 		print "\n TEST PROYECTO"
# 		print "\nBuscar Proyecto Creado"
# 		Proyecto.objects.create(nombre='project1', descripcion='p1',fechaCreacion='2015-04-09 21:03:31-04',fechaInicio='2015-04-09 21:03:31-04',fechaFin='2015-04-09 21:03:31-04',duracionEstimada='3',estado='ok')
# 		#dato={'nombre':'project1', 'descripcion':'p1', 'fechaCreacion':'2015-04-09 21:03:31-04', 'fechaInicio':'2015-04-09 21:03:31-04', 'fechaFin':'2015-04-09 21:03:31-04', 'duracionEstimada':'3', 'estado':'ok', 'usuarios':'1'}
# 	def test_traet(self):
# 		valido=False
# 		valido=Proyecto.objects.filter(nombre='project1').exists()
# 		if valido==False:
# 			print "\nNo existe el Proyecto"
# 		if valido == True:
# 			print "\nExiste el Proyecto"
#
#
#
# class TestProyectoNO(TestCase):
#
# 	def setUp(self):
# 		print "\n TEST PROYECTO no Existe"
# 		print "\nBuscar Proyecto Creado"
# 		Proyecto.objects.create(nombre='project1', descripcion='p1',fechaCreacion='2015-04-09 21:03:31-04',fechaInicio='2015-04-09 21:03:31-04',fechaFin='2015-04-09 21:03:31-04',duracionEstimada='3',estado='ok')
# 		#dato={'nombre':'project1', 'descripcion':'p1', 'fechaCreacion':'2015-04-09 21:03:31-04', 'fechaInicio':'2015-04-09 21:03:31-04', 'fechaFin':'2015-04-09 21:03:31-04', 'duracionEstimada':'3', 'estado':'ok', 'usuarios':'1'}
# 	def test_traet(self):
# 		valido=False
# 		valido=Proyecto.objects.filter(nombre='project2').exists()
# 		if valido==False:
# 			print "\nNo existe el Proyecto"
# 		if valido == True:
# 			print "\nExiste el Proyecto"
#
# ################################################################################################
# ######TEST Flujo
# ################################################################################################
#
# class TestFlujo(TestCase):
#
# 	def setUp(self):
# 		print "\n TEST Flujo Existe"
# 		print "\nBuscar Flujo Creado"
# 		Flujo.objects.create(nombre='flujo1')
# 		#dato={'nombre':'project1', 'descripcion':'p1', 'fechaCreacion':'2015-04-09 21:03:31-04', 'fechaInicio':'2015-04-09 21:03:31-04', 'fechaFin':'2015-04-09 21:03:31-04', 'duracionEstimada':'3', 'estado':'ok', 'usuarios':'1'}
# 	def test_traet(self):
# 		valido=False
# 		valido=Flujo.objects.filter(nombre='flujo1').exists()
# 		if valido==False:
# 			print "\nNo existe el Flujo"
# 		if valido == True:
# 			print "\nExiste el Flujo"
#
#
# class TestFlujoNO(TestCase):
#
# 	def setUp(self):
# 		print "\n TEST Flujo no Existe"
# 		print "\nBuscar Flujo Creado"
# 		Flujo.objects.create(nombre='flujo1')
# 		#dato={'nombre':'project1', 'descripcion':'p1', 'fechaCreacion':'2015-04-09 21:03:31-04', 'fechaInicio':'2015-04-09 21:03:31-04', 'fechaFin':'2015-04-09 21:03:31-04', 'duracionEstimada':'3', 'estado':'ok', 'usuarios':'1'}
# 	def test_traet(self):
# 		valido=False
# 		valido=Flujo.objects.filter(nombre='flujo23').exists()
# 		if valido==False:
# 			print "\nNo existe el Flujo"
# 		if valido == True:
# 			print "\nExiste el Flujo"
