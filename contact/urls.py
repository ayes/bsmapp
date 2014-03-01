from django.conf.urls import patterns, include, url
from contact import views

urlpatterns = patterns('',
	#url(r'^contact/main/?', 'contact.views.contacts_page'),
	url(r'^feedback', 'contact.views.feedback_page'),
)