from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^addEvent', views.addEvent, name='addEvent'),
    url(r'^addSlot', views.addSlot, name='addSlot'),
    url(r'^$', views.index, name='index'),      #NOTE This must be last otherwise it will always take precedent
]
