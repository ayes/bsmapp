from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^dashboard-cust/?', 'userdash.views.dashboard_cust'),
	url(r'^logout/?$','userdash.views.logout'),
	url(r'^domain-email/?', 'userdash.views.domain_email'),
	url(r'^user-email/?', 'userdash.views.user_email'),
	url(r'^edit-user-email/(?P<post_id>[\d]+)$', 'userdash.views.edit_user_email'),
	url(r'^add-user-email/?', 'userdash.views.add_user_email'),
	url(r'^create-user-email/?', 'userdash.views.create_user_email'),
)