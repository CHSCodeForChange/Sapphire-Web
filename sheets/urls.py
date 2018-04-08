from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^fromslot/(?P<slot_id>[0-9]+)/$', views.fromslot, name='fromslot'),
    url(r'^fromevent/(?P<event_id>[0-9]+)/$', views.fromevent, name='fromevent')

]
