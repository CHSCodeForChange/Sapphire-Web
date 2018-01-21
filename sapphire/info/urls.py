from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^overview/', views.overview, name='overview'),
    url(r'^codeforchange/', views.codeforchange, name='codeforchange')
]
