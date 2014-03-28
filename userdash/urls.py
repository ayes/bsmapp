from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^dashboard-cust/?$', 'userdash.views.dashboard_cust'),
	url(r'^dashboard-cust/logout/?$','userdash.views.logout'),

	# domain email
	url(r'^dashboard-cust/email/domain/?', 'userdash.views.domain_email'),
	url(r'^dashboard-cust/email/add-domain/?', 'userdash.views.add_domain_email'),
	url(r'^dashboard-cust/email/edit-domain/(?P<domain_id>[\d]+)$', 'userdash.views.edit_domain_email'),
	url(r'^dashboard-cust/email/delete-domain/(?P<domain_id>[\d]+)$', 'userdash.views.delete_domain_email'),
	url(r'^dashboard-cust/email/delete-confirm-domain?', 'userdash.views.delete_confirm_domain_email'),
	url(r'^dashboard-cust/email/error-domain/?', 'userdash.views.error_domain_email'),

	# user email
	url(r'^dashboard-cust/email/usermail/?', 'userdash.views.user_email'),
	url(r'^dashboard-cust/email/edit-usermail/(?P<post_id>[\d]+)$', 'userdash.views.edit_user_email'),
	url(r'^dashboard-cust/email/add-usermail/?', 'userdash.views.add_user_email'),
	url(r'^dashboard-cust/email/create-usermail/?', 'userdash.views.create_user_email'),
	url(r'^dashboard-cust/email/update-usermail/?', 'userdash.views.update_user_email'),
	url(r'^dashboard-cust/email/delete-usermail/(?P<usermail_id>[\d]+)$', 'userdash.views.delete_user_email'),
	url(r'^dashboard-cust/email/delete-confirm-usermail/?', 'userdash.views.delete_confirm_user_email'),

	# alias email
	url(r'^dashboard-cust/email/alias/?', 'userdash.views.email_alias'),

	# payment
	url(r'^dashboard-cust/management-payment/?', 'userdash.views.management_payment'),
	url(r'^dashboard-cust/deposit-paypal/?', 'userdash.views.deposit_paypal'),
	url(r'^dashboard-cust/cash-book/?', 'userdash.views.cash_book'),
	url(r'^dashboard-cust/cancel-deposit-paypal/?', 'userdash.views.cancel_deposit_paypal'),

	# profile customer
	url(r'^dashboard-cust/customer-profile/?', 'userdash.views.customer_profile'),
    url(r'^dashboard-cust/change-password/$', 'userdash.views.password_change', {'post_change_redirect' : '/dashboard-cust/change-password-done/', 'template_name': 'userdash_change_customer_password.html'}),
    url(r'^dashboard-cust/change-password-done/$', 'userdash.views.password_change_done', {'template_name': 'userdash_change_customer_password_done.html',}),
)

urlpatterns += patterns('',
    (r'^something/hard/to/guess/', include('paypal.standard.ipn.urls')),
)

