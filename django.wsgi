

import os
import imp
import sys

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sapphire.production")

application = get_wsgi_application()

application = DjangoWhiteNoise(application)
