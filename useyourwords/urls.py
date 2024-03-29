from django.conf.urls import patterns, include, url
from app.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^$', index),
	(r'^submit/', submit_text),
	(r'^submit-url/', submit_url),
    # Examples:
    # url(r'^$', 'useyourwords.views.home', name='home'),
    # url(r'^useyourwords/', include('useyourwords.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)
