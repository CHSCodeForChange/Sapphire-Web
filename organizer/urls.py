from django.conf.urls import url
from utility.models import Event, Slot
from django.views.generic import ListView, DetailView
from . import views




from . import views

urlpatterns = [
    url(r'^editSignIn/(?P<user_slot_id>[0-9]+)/$', views.editSignIn, name='editSignIn'),
    url(r'^editSignOut/(?P<user_slot_id>[0-9]+)/$', views.editSignOut, name='editSignOut'),
    url(r'^editField/(?P<user_slot_id>[0-9]+)/(?P<field>[\w\-]+)/$', views.editField, name='editField'),

    url(r'^editSlot/(?P<slot_id>[0-9]+)/$', views.editSlot, name='editSlot'),

    url(r'^addEvent/$', views.pick_group, name='pick_group'),
    url(r'^addEvent/(?P<group_id>[0-9]+)/$', views.addEvent, name='add_event'),
    url(r'^addUserSlot/(?P<slot_id>[0-9]+)/$', views.addUserSlot, name='add_user_slot'),
    url(r'^addUserManually/(?P<slot_id>[0-9]+)/$', views.addUserManually, name='addUserManually'),
    url(r'^addUserManually/(?P<slot_id>[0-9]+)/$', views.addUserManually, name='addUserManually'),
    url(r'^addSlot/(?P<event_id>[0-9]+)/$', views.addSlot, name='addSlot'),# DetailView.as_view(model = Event, template_name = "organizer/add_slot.html")), (?P<pk>\d+)/
    url(r'^addSingleSlot/$', views.pick_group, name='addSingleSlot'),# DetailView.as_view(model = Event, template_name = "organizer/add_slot.html")), (?P<pk>\d+)/
    url(r'^addSingleSlot/(?P<group_id>[0-9]+)/$', views.addSingleSlot, name='addSingleSlot'),# DetailView.as_view(model = Event, template_name = "organizer/add_slot.html")), (?P<pk>\d+)/

    url(r'^deleteUserSlot/(?P<user_slot_id>[0-9]+)/$', views.removeUserSlot, name='delete_user_slot'),
    url(r'^deleteEvent/(?P<event_id>[0-9]+)/$', views.deleteEvent, name='deleteEvent'),
    url(r'^deleteSlot/(?P<slot_id>[0-9]+)/$', views.deleteSlot, name='deleteSlot'),
    url(r'^event/(?P<event_id>[0-9]+)/console/$', views.console, name='console'),

    url(r'^updateEvent/(?P<event_id>[0-9]+)/$', views.editEvent, name='updateEvent'),
    url(r'^$', views.index, name='index'),      #NOTE This must be last otherwise it will always take precedent

    url(r'^sendMail/slot/(?P<slot_id>[0-9]+)/$', views.sendSlotOpeningNotification, name='sendSlotOpeningNotification'),
    url(r'^sendMail/event/(?P<event_id>[0-9]+)/$', views.sendEventOpeningNotification, name='sendEventOpeningNotification')
]
