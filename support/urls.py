from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^dashboard-cust/support/?$','support.views.support'),
	url(r'^dashboard-cust/add-support-ticket/?$','support.views.add_support_ticket'),
	url(r'^dashboard-cust/view-support-ticket/(?P<ticket_id>[\d]+)$','support.views.view_support_ticket'),
)