from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^$', 'acp.views.home_page', name = 'home'),
)
