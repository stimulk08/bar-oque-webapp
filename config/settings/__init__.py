from .security import *
from .middleware import MIDDLEWARE
from .templates import TEMPLATES
from .password_validators import AUTH_PASSWORD_VALIDATORS
from .local import *
from .drf import REST_FRAMEWORK
from .installed_apps import INSTALLED_APPS
from .cors import *


ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if DEBUG:
    from .development import *
    from .open_api import *
else:
    from .production import *
