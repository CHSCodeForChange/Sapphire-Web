from django.conf.urls import url

from . import views
from feed.models import Feed_Entry
from django.views.generic import ListView, DetailView


urlpatterns = [
    url(r'^$', views.feed, name='feed'),
    url(r'^group/(?P<group_id>[0-9]+)/$$', views.filterByGroup, name='filterByGroup'),
]
