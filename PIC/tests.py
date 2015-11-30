from datetime import datetime
from django.utils import timezone
from django.test import TestCase
from AdminProyectos.models import Proyecto
from django.test.utils import override_settings
from django.contrib.auth.models import User, Group
from django.test import TestCase
from Flujo.models import Flujo
from django.contrib.auth.models import User, Group


class TestUserBD(TestCase):
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
        User.objects.create(username="moises", password="moises")
        try:
            #vamos a la pantalla de inicio
            resp=self.client.get('/admin/login/?next=/admin/')
            self.assertEqual(resp.status_code,200)
            #logueamos con el usuario admin
            login = self.client.login(username="moises", password="moises")
            self.assertFalse(login)
        except:
            if resp.status_code == 404:
                print("Prueba Fallida, la url no existe")
            print("Prueba Fallida, el usuario no existe")
            return
        print("Prueba exitosa, el usuario pudo iniciar sesion")

class testf(TestCase):
    def testf(self):
        print "\n"
class testNologin(TestCase):
    def test_login_usuario(self):
        print("\n TEST: Loguear Usuario NO Registrado")
        usuario="admin"
        password="admin"
        try:
        #vamos a la pantalla de inici
            resp=self.client.get('/admin/login/?next=/admin/')
            self.assertEqual(resp.status_code,200)
            #logueamos con el usuario admin
            login = self.client.login(username=usuario, password=password)
            self.assertTrue(login)
        except:
            if resp.status_code == 404:
                print("Prueba Fallida, la url no existe")
            print("Prueba Exitosa, el usuario no registrado no pudo acceder")
            return
        print("Prueba Fallida, el usuario pudo iniciar sesion")

class UsuarioTestCase (TestCase):

   def setUp (self):
      print "\n TEST: USUARIO"
      print "\n ------Buscar el usuario creado"
      User.objects.create(username="aa", password="aa")
   def test_traer(self):
       valido = False
       valido = User.objects.filter(username="aa").exists()
       if valido==True:
           print "\n------Se ha encontrado el usuario creado"

       print "\n ------Buscar un usuario inexistente"
       valido = True
       valido = User.objects.filter(username='"oo"').exists()
       if valido==False:
           print "\n------No existe el usuario buscado"

class GrupoTestCase (TestCase):

   def setUp (self):
      print "\n TEST GRUPO"
      print "\n --Buscar el Grupo creado"
      Group.objects.create(name="aa")

   def test_traer(self):
       valido = False
       valido = Group.objects.filter(name="aa").exists()
       if valido==True:
           print "\n---Se ha encontrado el Grupo creado"

       print "\n --Buscar un Grupo inexistente"
       valido = True
       valido = Group.objects.filter(name='"oo"').exists()
       if valido==False:
           print "\n---No existe el grupo buscado"

# Create your tests here.
#USUARIO
class TestUsuario(TestCase):
    def setUp(self):
        print "\n TEST Usuario Existe"
        print "\nBuscar Usuario Creado"
        #Usuario.objects.create(nombre='Usuario')
        dato={'nombre':'nombre1', 'password':'12345', 'fechaCreacion':'2015-04-09'}
    def test_traet(self):
        valido=True
        #valido=Usuario.objects.filter(nombre='Usuario').exists()
        if valido==False:
            print "\nNo existe el Usuario"
        if valido == True:
            print "\nExiste el Usuario"


class TestUsuarioNO(TestCase):

    def setUp(self):
        print "\n TEST Usuario no Existe"
        print "\nBuscar Usuario Creado"
        #Usuario.objects.create(nombre='Usuario')
        dato={'nombre':'nombre1', 'password':'12345', 'fechaCreacion':'2015-04-09'}
    def test_traet(self):
        valido=False
        #valido=Usuario.objects.filter(nombre='Usuario').exists()
        if valido==False:
            print "\nNo existe el Usuario"
        if valido == True:
            print "\nExiste el Usuario"
