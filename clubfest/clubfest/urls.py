"""clubfest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'parakeet.views.index'),
    url(r'^upload/', 'parakeet.views.upload'),
    url(r'^([0-9]+)$', 'parakeet.views.index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^mapgen/$', 'parakeet.views.mapgen'),
    url(r'^mapgen/(?P<row>[0-9]+)_(?P<col>[0-9]+)$', 'parakeet.views.mapgen'),
    url(r'^login/', 'parakeet.views.admin_login'),
    url(r'^club_index/', 'parakeet.views.clubindex')
]
