from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^fromSlot/(?P<slot_id>[0-9]+)/$', views.from_slot, name='from_slot'),
    url(r'^fromEvent/(?P<event_id>[0-9]+)/$', views.from_event, name='from_event')

]
