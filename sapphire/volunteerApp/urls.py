from django.conf.urls import url

from . import views
from utility.models import Event, Slot
from django.views.generic import ListView, DetailView


urlpatterns = [
    url(r'^calendar/', views.calendar, name='calendar'),
    url(r'^eventNeeds/', views.eventNeeds, name='eventNeeds'),
    url(r'^event/(?P<pk>\d+)$', DetailView.as_view(context_object_name="event", model = Event, template_name = "volunteer/event.html"), name='eventView'),
    url(r'^slot/(?P<pk>\d+)$', DetailView.as_view(context_object_name="slot", model = Slot, template_name = "volunteer/slot.html"), name='slotView'), #We should make this start with eventView instead of just having numbers
    url(r'^slots/', views.slotNeeds, name='slotNeeds'),
    url(r'^$', views.index, name='index'),      #NOTE This must be last otherwise it will always take precedent
    url(r'^slot/(?P<slot_id>[0-9]+)/volunteer$', views.volunteer, name='volunteer'), #We should make this start with eventView instead of just having numbers
    #url(r'^slot/(?P<slot_id>[0-9]+)/$', views.volunteer, name='volunteer'),
]
