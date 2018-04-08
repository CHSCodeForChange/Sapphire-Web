from django.conf.urls import url

from . import views
from utility.models import Event, Slot
from django.views.generic import ListView, DetailView


urlpatterns = [
    url(r'^calendar/', views.calendar, name='calendar'),
    url(r'^eventNeeds/', views.eventNeeds, name='eventNeeds'),
    url(r'^event/(?P<event_id>[0-9]+)$', views.event, name='eventView'),
    url(r'^slot/(?P<slot_id>[0-9]+)$', views.slot, name='slotView'),
    url(r'^slots/', views.slotNeeds, name='slotNeeds'),
    url(r'^$', views.index, name='index'),      #NOTE This must be last otherwise it will always take precedent
    url(r'^slot/(?P<slot_id>[0-9]+)/volunteer/$', views.volunteer, name='volunteer'), #We should make this start with eventView instead of just having numbers
    url(r'^slot/(?P<slot_id>[0-9]+)/volunteer/(?P<user_id>[0-9]+)/$', views.volunteerForUser, name='volunteerForUser'), #We should make this start with eventView instead of just having numbers
    url(r'^slot/(?P<slot_id>[0-9]+)/unvolunteer/$', views.unvolunteer, name='unvolunteer'), #We should make this start with eventView instead of just having numbers
    url(r'^signin/(?P<user_slot_id>[0-9]+)$', views.signin, name='signin'), #We should make this start with eventView instead of just having numbers
    url(r'^signout/(?P<user_slot_id>[0-9]+)$', views.signout, name='signout'), #We should make this start with eventView instead of just having numbers


    #url(r'^slot/(?P<slot_id>[0-9]+)/$', views.volunteer, name='volunteer'),

]
