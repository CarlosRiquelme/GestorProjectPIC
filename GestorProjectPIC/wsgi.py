# -.- coding: utf-8 -.-
import os, sys
from GestorProjectPIC import settings
 
path = settings.PATH
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GestorProjectPIC.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
