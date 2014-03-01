from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^dashboard-cust/?$', 'userdash.views.dashboard_cust'),
	url(r'^dashboard-cust/logout/?$','userdash.views.logout'),
	url(r'^dashboard-cust/domain-email/?', 'userdash.views.domain_email'),
	url(r'^dashboard-cust/user-email/?', 'userdash.views.user_email'),
	url(r'^dashboard-cust/edit-user-email/(?P<post_id>[\d]+)$', 'userdash.views.edit_user_email'),
	url(r'^dashboard-cust/add-user-email/?', 'userdash.views.add_user_email'),
	url(r'^dashboard-cust/create-user-email/?', 'userdash.views.create_user_email'),
	url(r'^dashboard-cust/update-user-email/?', 'userdash.views.update_user_email'),
	url(r'^dashboard-cust/kelola-pembayaran/?', 'userdash.views.kelola_pembayaran'),
)