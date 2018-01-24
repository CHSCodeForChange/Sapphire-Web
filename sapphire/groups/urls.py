from django.conf.urls import url

from . import views
from feed.models import Feed_Entry
from django.views.generic import ListView, DetailView
from .models import Group


urlpatterns = [
    url(r'^$', views.list, name='list'),
    url(r'^add/', views.add, name='add'),
    url(r'^(?P<pk>\d+)/', DetailView.as_view(context_object_name="group", model = Group, template_name = "groups/groupView.html"), name='groupView'),
]
