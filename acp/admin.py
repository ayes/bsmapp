# -*- coding: utf-8 -*-

from django import forms
from django.contrib import admin
#from django.contrib.auth.models import Group
from acp.models import *

class MailDomainAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'notes', 'user', 'position')
	list_editable = ('position',)

	fieldsets = (
		('', {
			'fields': ('domain', 'user', 'notes'),
		}),
	)

	class Media:
		js = ['/static/js/admin_list_reorder.js',]

class MailUserAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'domain', 'mailbox_size', 'active')
	list_filter = ('domain',)

class MailQuotaAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'price')

class MailAliasAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'destination_address')

admin.site.register(MailDomain, MailDomainAdmin)
admin.site.register(MailUser, MailUserAdmin)
admin.site.register(MailQuota, MailQuotaAdmin)
admin.site.register(MailAlias, MailAliasAdmin)

#admin.site.unregister(Group)
