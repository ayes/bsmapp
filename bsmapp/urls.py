from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'portal.views.main', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(.*)$', 'django.views.static.serve', {'document_root' : settings.MEDIA_ROOT}),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'', include('portal.urls')),
    url(r'', include('blog.urls')),
    url(r'', include('register.urls')),
    url(r'', include('userdash.urls')),
    url(r'', include('support.urls')),
)
