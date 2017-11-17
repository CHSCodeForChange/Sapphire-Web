from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^feed/', views.feed, name='feed'),
    url(r'^calendar/', views.calendar, name='calendar'),
    url(r'^eventNeeds/', views.eventNeeds, name='eventNeeds'),
    url(r'^slotNeeds/', views.slotNeeds, name='slotNeeds'),
    url(r'^$', views.index, name='index'),      #NOTE This must be last otherwise it will always take precedent
]
