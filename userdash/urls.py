from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^dashboard-cust/?$', 'userdash.views.dashboard_cust'),
	url(r'^dashboard-cust/logout/?$','userdash.views.logout'),

	# domain
	url(r'^dashboard-cust/domain-email/?', 'userdash.views.domain_email'),
	url(r'^dashboard-cust/add-domain-email/?', 'userdash.views.add_domain_email'),
	url(r'^dashboard-cust/edit-domain-email/(?P<domain_id>[\d]+)$', 'userdash.views.edit_domain_email'),
	url(r'^dashboard-cust/delete-domain-email/(?P<domain_id>[\d]+)$', 'userdash.views.delete_domain_email'),
	url(r'^dashboard-cust/delete-confirm-domain-email/?', 'userdash.views.delete_confirm_domain_email'),
	url(r'^dashboard-cust/error-domain-email/?', 'userdash.views.error_domain_email'),

	# user email
	url(r'^dashboard-cust/user-email/?', 'userdash.views.user_email'),
	url(r'^dashboard-cust/edit-user-email/(?P<post_id>[\d]+)$', 'userdash.views.edit_user_email'),
	url(r'^dashboard-cust/add-user-email/?', 'userdash.views.add_user_email'),
	url(r'^dashboard-cust/create-user-email/?', 'userdash.views.create_user_email'),
	url(r'^dashboard-cust/update-user-email/?', 'userdash.views.update_user_email'),
	url(r'^dashboard-cust/delete-user-email/(?P<usermail_id>[\d]+)$', 'userdash.views.delete_user_email'),
	url(r'^dashboard-cust/delete-confirm-user-email/?', 'userdash.views.delete_confirm_user_email'),

	# payment
	url(r'^dashboard-cust/management-payment/?', 'userdash.views.management_payment'),
	url(r'^dashboard-cust/deposit-paypal/?', 'userdash.views.deposit_paypal'),
	url(r'^dashboard-cust/cash-book/?', 'userdash.views.cash_book'),
	url(r'^dashboard-cust/cancel-deposit-paypal/?', 'userdash.views.cancel_deposit_paypal'),

	# profile customer
	url(r'^dashboard-cust/customer-profile/?', 'userdash.views.customer_profile'),
	url(r'^dashboard-cust/change-password/$', 'django.contrib.auth.views.password_change', {'post_change_redirect' : '/dashboard-cust/change-password-done/', 'template_name': 'userdash_change_customer_password.html',}),
    url(r'^dashboard-cust/change-password-done/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'userdash_change_customer_password_done.html',}),
)

urlpatterns += patterns('',
    (r'^something/hard/to/guess/', include('paypal.standard.ipn.urls')),
)

