from django.conf.urls import patterns, include, url
from register import views

urlpatterns = patterns('',
	url(r'^register/?', 'register.views.register'),
)