from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^dashboard-cust/support/?$','support.views.support'),
	url(r'^dashboard-cust/add-support-ticket/?$','support.views.add_support_ticket'),
)