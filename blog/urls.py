from django.conf.urls import patterns, include, url
from blog import views

urlpatterns = patterns('',
	url(r'^blog/?', 'blog.views.blog'),
	url(r'^category-blog/(?P<kategori_id>[\d]+)$', 'blog.views.blog_category'),
	url(r'^read-blog/(?P<post_id>[\d]+)$', 'blog.views.blog_read'),
)