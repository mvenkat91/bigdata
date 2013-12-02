import os
import sys
sys.path.append(os.path.abspath('.'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from home.models import *
from home.util import *

