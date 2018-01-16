from django.conf.urls import url
from utility.models import Event, Slot
from django.views.generic import ListView, DetailView
from . import views




from . import views

urlpatterns = [
    url(r'^add/$', views.add, name='add'),
    url(r'^addSlot$', views.addSlot, name='addSlot'),# DetailView.as_view(model = Event, template_name = "organizer/add_slot.html")), (?P<pk>\d+)/
    url(r'^deleteEvent/(?P<event_id>[0-9]+)/$', views.deleteEvent, name='deleteEvent'),
    url(r'^$', views.index, name='index'),      #NOTE This must be last otherwise it will always take precedent
]
