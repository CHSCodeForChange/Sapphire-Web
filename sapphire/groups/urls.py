from django.conf.urls import url

from . import views
from feed.models import Feed_Entry
from django.views.generic import ListView, DetailView
from .models import Group


urlpatterns = [
    url(r'^$', views.list, name='list'),
    url(r'^add/', views.add, name='add'),
    url(r'^(?P<group_id>[0-9]+)/join/$', views.join, name='joinGroup'),
    url(r'^(?P<group_id>[0-9]+)/$', views.group, name='groupView'),
]
