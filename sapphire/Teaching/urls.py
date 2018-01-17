from django.conf.urls import url

from . import views
from Teaching.models import Animal

urlpatterns = [
    url(r'^animal/', views.animal, name='animal'),
]
