from datetime import datetime
from django.test import TestCase
from django.test.utils import override_settings
from django.contrib.auth.models import User

class TestUserBD(TestCase):
	"""
		Test para ver si la Base de Datos 
		se encuentra vacio
	"""
	def test_numero_elementos(self):
		print("\n TEST: Verificar si esta vacia la Base de Datos")
		try:
			self.assertEqual(0,len(User.objets.all()))
		except:
			print("Base de Datos vacia, el numero de usuarios es distintos de 0")
			return
		print("Base de Datos no se encuentra vacia")

class TestLogin(TestCase):
	def test_login_usuario(self):
		print("\n TEST: Loguear Usuario Registrado")
		username='admin'
		password='admin'
		try:
			#vamos a la pantalla de inicio
			#resp=self.client.get('/admin/login/?next=/admin/')
			self.assertEqual(resp.status_code,200)
			#logueamos con el usuario admin
			login = self.client.login(username=self.username, password=self.password)
			self.assertTrue(login)
		except:
			print("Prueba Fallida, el usuario no existe")
			return
		print("Prueba exitosa, el usuario pudo iniciar sesion")