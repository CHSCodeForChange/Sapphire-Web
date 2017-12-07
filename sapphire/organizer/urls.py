from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^add/$', views.add, name='add'),
    url(r'^deleteEvent/(?P<event_id>[0-9]+)/$', views.deleteEvent, name='deleteEvent'),
    url(r'^$', views.index, name='index'),      #NOTE This must be last otherwise it will always take precedent
]
