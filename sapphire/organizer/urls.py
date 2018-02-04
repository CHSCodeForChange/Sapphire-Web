from django.conf.urls import url
from utility.models import Event, Slot
from django.views.generic import ListView, DetailView
from . import views




from . import views

urlpatterns = [
    url(r'^addEvent/$', views.pick_group, name='pick_group'),
    url(r'^addEvent/(?P<group_id>[0-9]+)/$', views.addEvent, name='add_event'),
    url(r'^addSlot/(?P<event_id>[0-9]+)/$', views.addSlot, name='addSlot'),# DetailView.as_view(model = Event, template_name = "organizer/add_slot.html")), (?P<pk>\d+)/
    url(r'^deleteEvent/(?P<event_id>[0-9]+)/$', views.deleteEvent, name='deleteEvent'),
    url(r'^deleteSlot/(?P<slot_id>[0-9]+)/$', views.deleteSlot, name='deleteSlot'),
    url(r'^$', views.index, name='index'),      #NOTE This must be last otherwise it will always take precedent
]
