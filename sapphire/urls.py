"""sapphire URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views

from accounts.forms import LoginForm

urlpatterns = [
    url(r'^bs/$', auth_views.login, {'template_name': 'bs-4-header.html'}, name='bs-4'), #, 'authentication_form': LoginForm
    url(r'^admin/', admin.site.urls),
    url(r'^feed/', include('feed.urls')),
    url(r'^info/', include('info.urls')),
    url(r'^groups/', include('groups.urls')),
    url(r'^sheets/', include('sheets.urls')),
    url(r'^volunteer/', include('volunteer.urls')),
    url(r'^organizer/', include('organizer.urls')),
    url(r'^$', views.home, name='home'),
    url(r'^home/', include('volunteer.urls')),           #TODO this should be set programatically depending on auth type
    url(r'^login/$', auth_views.login, {'template_name': 'accounts/login.html'}, name='login'), #, 'authentication_form': LoginForm
    url(r'^logout/$', auth_views.logout, {'next_page' : '/accounts/logout_lander'}, name='logout'),    # Will redirect to the next page
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    # url(r'^', auth_views.login, {'template_name' : 'auth/login.html'}, name='login'),   #TODO this should remember you are logged in
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
