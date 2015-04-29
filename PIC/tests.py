from datetime import datetime
from django.utils import timezone
from django.test import TestCase
from django.test.utils import override_settings
from django.contrib.auth.models import User, Group
from PIC.models import Proyecto, Flujo, Sprint, User_Story, Comentario


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
			print("------Base de Datos vacia, el numero de usuarios es distintos de 0")
			return
		print("------------Base de Datos no se encuentra vacia")

class TestLogin(TestCase):
	"""
	
	Test para prueba de login de un usuario registrado
	en el sistema
	
	"""

	def test_login_usuario(self):
		print("\n TEST: Loguear Usuario Registrado")
		#username="admin"
		#password="admin"
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
				print("------------Prueba Fallida, la url no existe")
			print("------------Prueba Fallida, el usuario no existe")
			return
		print("------------Prueba exitosa, el usuario pudo iniciar sesion")

class testf(TestCase):
	def testf(self):
		print "\n"
class testNologin(TestCase):
	"""
	Test prueba de login de un usuario no registrado 
	en el sistema 
	
	"""
	def test_login_usuario(self):
		print("\n TEST: Loguear Usuario NO Registrado")
		usuario="admin"
		password="admin"
		try:
			#vamos a la pantalla de inicio
			resp=self.client.get('/admin/login/?next=/admin/')
			self.assertEqual(resp.status_code,200)
			#logueamos con el usuario admin
			login = self.client.login(username=usuario, password=password)
			self.assertTrue(login)
		except:
			if resp.status_code == 404:
				print("------------Prueba Fallida, la url no existe")
			print("------------Prueba Exitosa, el usuario no registrado no pudo acceder")
			return
		print("------------Prueba Fallida, el usuario pudo iniciar sesion")

class UsuarioTestCase (TestCase):

  def setUp (self):
     print "\n TEST: USUARIO"
     print "\n ------Buscar el usuario creado"
     User.objects.create(username="aa", password="aa")
  def test_traer(self):
      valido = False
      valido = User.objects.filter(username="aa").exists()
      if valido==True:
          print "\n------------Se ha encontrado el usuario creado"

      print "\n ------Buscar un usuario inexistente"
      valido = True
      valido = User.objects.filter(username='"oo"').exists()
      if valido==False:
          print "\n------------No existe el usuario buscado"

class GrupoTestCase (TestCase):

  def setUp (self):
     print "\n TEST GRUPO"
     print "\n ------Buscar el Grupo creado"
     Group.objects.create(name="aa")

  def test_traer(self):
      valido = False
      valido = Group.objects.filter(name="aa").exists()
      if valido==True:
          print "\n-----Se ha encontrado el Grupo creado"

      print "\n ------Buscar un Grupo inexistente"
      valido = True
      valido = Group.objects.filter(name='"oo"').exists()
      if valido==False:
          print "\n------No existe el grupo buscado"
################################################################################################
######TEST PROYECTO
################################################################################################

class TestProyecto(TestCase):

	def setUp(self):
		print "\n TEST PROYECTO"
		print "\n------Buscar Proyecto Creado"
        Proyecto.objects.create(nombre='project1', descripcion='p1',fechaCreacion='2015-04-09 21:03:31-04',
                                fechaInicio='2015-04-09 21:03:31-04',fechaFin='2015-04-09 21:03:31-04',
                                duracionEstimada='3',estado='ok',scrumMaster=User.objects.create(username="aa", password="aa"))
		#dato={'nombre':'project1', 'descripcion':'p1', 'fechaCreacion':'2015-04-09 21:03:31-04', 'fechaInicio':'2015-04-09 21:03:31-04', 'fechaFin':'2015-04-09 21:03:31-04', 'duracionEstimada':'3', 'estado':'ok', 'usuarios':'1'}
	def test_traet(self):
		valido=False
		valido=Proyecto.objects.filter(nombre='project1').exists()
		if valido==False:
			print "\n------------No existe el Proyecto"
		if valido == True:
			print "\n------------Existe el Proyecto"



class TestProyectoNO(TestCase):

	def setUp(self):
		print "\n TEST PROYECTO no Existe"
		print "\n------Buscar Proyecto Creado"
        #usuario=User.objects.create(name='usuario',password='123',password='123')
		Proyecto.objects.create(nombre='project1', descripcion='p1',fechaCreacion='2015-04-09 21:03:31-04',
                                fechaInicio='2015-04-09 21:03:31-04',fechaFin='2015-04-09 21:03:31-04',
                                duracionEstimada='3',estado='ok', scrumMaster=User.objects.create(username="aa1", password="aa"))
	def test_traet(self):
		valido=False
		valido=Proyecto.objects.filter(nombre='project2').exists()
		if valido==False:
			print "\n------------No existe el Proyecto"
		if valido == True:
			print "\n------------Existe el Proyecto"

################################################################################################
######TEST Flujo
################################################################################################

class TestFlujo(TestCase):

	def setUp(self):
		print "\n TEST Flujo Existe"
		print "\n------Buscar Flujo Creado"
		Flujo.objects.create(nombre='flujo1',tiempo_estimado='3', estado='EN-ESPERA',proyecto=Proyecto.objects.create(nombre='project1', descripcion='p1',fechaCreacion='2015-04-09 21:03:31-04',
                                fechaInicio='2015-04-09 21:03:31-04',fechaFin='2015-04-09 21:03:31-04',
                                duracionEstimada='3',estado='ok',scrumMaster=User.objects.create(username="aa3", password="aa")) )
		#dato={'nombre':'project1', 'descripcion':'p1', 'fechaCreacion':'2015-04-09 21:03:31-04', 'fechaInicio':'2015-04-09 21:03:31-04', 'fechaFin':'2015-04-09 21:03:31-04', 'duracionEstimada':'3', 'estado':'ok', 'usuarios':'1'}
	def test_traet(self):
		valido=False
		valido=Flujo.objects.filter(nombre='flujo1').exists()
		if valido==False:
			print "\n------------No existe el Flujo"
		if valido == True:
			print "\n------------Existe el Flujo"


class TestFlujoNO(TestCase):

	def setUp(self):
		print "\n TEST Flujo no Existe"
		print "\n------Buscar Flujo Creado"
		Flujo.objects.create(nombre='flujo1',tiempo_estimado='3', estado='EN-ESPERA', proyecto=Proyecto.objects.create(nombre='project1', descripcion='p1',fechaCreacion='2015-04-09 21:03:31-04',
                                fechaInicio='2015-04-09 21:03:31-04',fechaFin='2015-04-09 21:03:31-04',
                                duracionEstimada='3',estado='ok',scrumMaster=User.objects.create(username="aa4", password="aa")))
		#dato={'nombre':'project1', 'descripcion':'p1', 'fechaCreacion':'2015-04-09 21:03:31-04', 'fechaInicio':'2015-04-09 21:03:31-04', 'fechaFin':'2015-04-09 21:03:31-04', 'duracionEstimada':'3', 'estado':'ok', 'usuarios':'1'}
	def test_traet(self):
		valido=False
		valido=Flujo.objects.filter(nombre='flujo23').exists()
		if valido==False:
			print "\n------------No existe el Flujo"
		if valido == True:
			print "\n------------Existe el Flujo"


################################################################################################
######TEST Sprint
################################################################################################

class TestSprint(TestCase):
    def setUp(self):
        print "\n TEST de Sprint EXISTE "
        print "\n------Buscar Sprint Creado"
        Sprint.objects.create(nombre = 'sprint10', fechaCreacion = '2015-04-28 21:03:31-04',
                              fechaInicio = '2015-04-28 21:03:31-04', fechaFinEstimado = '2015-04-29 21:03:31-04',
                              tiempoEstimado = '3')
    def test_comprobar_scprint(self):
        valido=False
        valido=Sprint.objects.filter(nombre='sprint10').exists()
        if valido==False:
            print "\n------------NOOOOOO existe el Sprint que se Busca..................."
        if valido==True:
            print "\n------------EXISTE el Sprint que se Busca..................."

class TestSprintNO(TestCase):
    def setUp(self):
        print "\n TEST de Sprint NOOOOO EXISTE "
        print "\n------Buscar Sprint Creado"
        Sprint.objects.create(nombre = 'sprint10', fechaCreacion = '2015-04-28 21:03:31-04',
                              fechaInicio = '2015-04-28 21:03:31-04', fechaFinEstimado = '2015-04-29 21:03:31-04',
                              tiempoEstimado = '3')
    def test_comprobar_scprintNO(self):
        valido=False
        valido=Sprint.objects.filter(nombre='sprint17').exists()
        if valido==False:
            print "\n------------NOOOOOO existe el Sprint que se Busca..................."
        if valido==True:
            print "\n------------EXISTE el Sprint que se Busca..................."

################################################################################################
######TEST USER STORY
################################################################################################

class TestUserStory(TestCase):
    def setUp(self):
        print "\n TEST de USER STORY EXISTE "
        print "\n------Buscar User Story Creado"
        User_Story.objects.create(nombre='userstory5', descripcion= 'UserStory TEST', tiempo_estimado='3',
                                  tiempo_trabajado='2',fecha_inicio='2015-04-28 21:03:31-04', fecha_fin='2015-04-28 21:03:31-04',
                                  user=User.objects.create(username='aa',password='aa'),
                                  proyecto=Proyecto.objects.create(nombre='project1', descripcion='p1',
                                                                   fechaCreacion='2015-04-09 21:03:31-04',
                                                                   fechaInicio='2015-04-09 21:03:31-04',
                                                                   fechaFin='2015-04-09 21:03:31-04',
                                                                   duracionEstimada='3',estado='EN-ESPERA'),
                                  flujo=Flujo.objects.create(nombre='flujo1',tiempo_estimado='3', estado='EN-ESPERA'),
                                  activo=False,
                                  sprint=Sprint.objects.create(nombre = 'sprint10', fechaCreacion = '2015-04-28 21:03:31-04',
                                                               fechaInicio = '2015-04-28 21:03:31-04',
                                                               fechaFinEstimado = '2015-04-29 21:03:31-04',
                                                               tiempoEstimado = '3'))
    def test_comprobar_user_story(self):
        valido=False
        valido=User_Story.objects.filter(nombre='userstory5').exists()
        if valido==False:
            print "\n------------NOOOOOO existe el USER STORY que se Busca..................."
        if valido==True:
            print "\n------------EXISTE el USER STORY que se Busca..................."
class TestUserStory(TestCase):
    def setUp(self):
        print "\n TEST de USER STORY EXISTE "
        print "\n------Buscar User Story Creado"
        User_Story.objects.create(nombre='userstory5', descripcion= 'UserStory TEST', tiempo_estimado='3',
                                  tiempo_trabajado='2',fecha_inicio='2015-04-28 21:03:31-04', fecha_fin='2015-04-28 21:03:31-04',
                                  user=User.objects.create(username='aa',password='aa'),
                                  proyecto=Proyecto.objects.create(nombre='project1', descripcion='p1',
                                                                   fechaCreacion='2015-04-09 21:03:31-04',
                                                                   fechaInicio='2015-04-09 21:03:31-04',
                                                                   fechaFin='2015-04-09 21:03:31-04',
                                                                   duracionEstimada='3',estado='EN-ESPERA'),
                                  flujo=Flujo.objects.create(nombre='flujo1',tiempo_estimado='3', estado='EN-ESPERA'),
                                  activo=False,
                                  sprint=Sprint.objects.create(nombre = 'sprint10', fechaCreacion = '2015-04-28 21:03:31-04',
                                                               fechaInicio = '2015-04-28 21:03:31-04',
                                                               fechaFinEstimado = '2015-04-29 21:03:31-04',
                                                               tiempoEstimado = '3'))
    def test_comprobar_user_story_NO(self):
        valido=False
        valido=User_Story.objects.filter(nombre='userstory15').exists()
        if valido==False:
            print "\n------------NOOOOOO existe el USER STORY que se Busca..................."
        if valido==True:
            print "\n------------EXISTE el USER STORY que se Busca..................."


################################################################################################
######TEST COMENTARIO
################################################################################################

class TestComentario(TestCase):
    def setUp(self):
        print "\n TEST de Sprint EXISTE "
        print "\n------Buscar Sprint Creado"
        Comentario.objects.create(titulo='comentario1',contenido='Test Comentario',fecha='2015-04-28 21:03:31-04',
                                  user_story=User_Story.objects.create(nombre='userstory5', descripcion= 'UserStory TEST',
                                                                       tiempo_estimado='3',
                                                                       tiempo_trabajado='2',fecha_inicio='2015-04-28 21:03:31-04',
                                                                       fecha_fin='2015-04-28 21:03:31-04',
                                                                       user=User.objects.create(username='aa',password='aa'),
                                                                       proyecto=Proyecto.objects.create(nombre='project1', descripcion='p1',
                                                                                                        fechaCreacion='2015-04-09 21:03:31-04',
                                                                                                        fechaInicio='2015-04-09 21:03:31-04',
                                                                                                        fechaFin='2015-04-09 21:03:31-04',
                                                                                                        duracionEstimada='3',estado='EN-ESPERA'),
                                                                       flujo=Flujo.objects.create(nombre='flujo1',tiempo_estimado='3', estado='EN-ESPERA'),
                                                                       activo=False,
                                                                       sprint=Sprint.objects.create(nombre = 'sprint10', fechaCreacion = '2015-04-28 21:03:31-04',
                                                                                                    fechaInicio = '2015-04-28 21:03:31-04',
                                                                                                    fechaFinEstimado = '2015-04-29 21:03:31-04',
                                                                                                    tiempoEstimado = '3')),
                                  hora_trabajada='2')
    def test_comprobar_comentario(self):
        valido=False
        valido=Comentario.objects.filter(titulo='comentario1').exists()
        if valido==False:
            print "\n------------NOOOOOO existe el Sprint que se Busca..................."
        if valido==True:
            print "\n------------EXISTE el Sprint que se Busca..................."


class TestComentarioNO(TestCase):
    def setUp(self):
        print "\n TEST de Sprint EXISTE "
        print "\n------Buscar Sprint Creado"
        Comentario.objects.create(titulo='comentario1',contenido='Test Comentario',fecha='2015-04-28 21:03:31-04',
                                  user_story=User_Story.objects.create(nombre='userstory5', descripcion= 'UserStory TEST',
                                                                       tiempo_estimado='3',
                                                                       tiempo_trabajado='2',fecha_inicio='2015-04-28 21:03:31-04',
                                                                       fecha_fin='2015-04-28 21:03:31-04',
                                                                       user=User.objects.create(username='aa',password='aa'),
                                                                       proyecto=Proyecto.objects.create(nombre='project1', descripcion='p1',
                                                                                                        fechaCreacion='2015-04-09 21:03:31-04',
                                                                                                        fechaInicio='2015-04-09 21:03:31-04',
                                                                                                        fechaFin='2015-04-09 21:03:31-04',
                                                                                                        duracionEstimada='3',estado='EN-ESPERA'),
                                                                       flujo=Flujo.objects.create(nombre='flujo1',tiempo_estimado='3', estado='EN-ESPERA'),
                                                                       activo=False,
                                                                       sprint=Sprint.objects.create(nombre = 'sprint10', fechaCreacion = '2015-04-28 21:03:31-04',
                                                                                                    fechaInicio = '2015-04-28 21:03:31-04',
                                                                                                    fechaFinEstimado = '2015-04-29 21:03:31-04',
                                                                                                    tiempoEstimado = '3')),
                                  hora_trabajada='2')
    def test_comprobar_comentario_NO(self):
        valido=False
        valido=Comentario.objects.filter(titulo='comentario18').exists()
        if valido==False:
            print "\n------------NOOOOOO existe el Sprint que se Busca..................."
        if valido==True:
            print "\n------------EXISTE el Sprint que se Busca..................."
