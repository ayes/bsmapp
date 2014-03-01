from django.conf.urls import patterns, include, url
from portal import views
#from contact import views

urlpatterns = patterns('',
	url(r'^product/faza-shop/?', 'portal.views.fazashop'),
	url(r'^product/bsm-retail-pos/?', 'portal.views.bsmretailpos'),
	url(r'^service/web-development/?', 'portal.views.webdevelopment'),
	url(r'^service/mail-server/?', 'portal.views.mailserver'),
	url(r'^service/radio-streaming/?', 'portal.views.radiostreaming'),
	url(r'^labs/zamanda/?', 'portal.views.labs_zamanda'),
	url(r'^labs/siak/?', 'portal.views.labs_siak'),
	url(r'^contact-us/?', 'contact.views.contacts_page'),
	#url(r'^contact_us/?', 'portal.views.contact_us'),
	url(r'^about-us/?', 'portal.views.about_us'),
	url(r'^search/$', 'portal.views.search'),
	url(r'^portfolio/?', 'portal.views.portfolio'),
	url(r'^download/?', 'portal.views.ratudewi_download'),
	url(r'^single-download/?', 'portal.views.download_view'),
	url(r'^login/?', 'portal.views.login'),
)