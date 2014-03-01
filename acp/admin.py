# -*- coding: utf-8 -*-

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from models import *

class MailDomainAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'notes', 'position')
	list_editable = ('position',)

	fieldsets = (
		('', {
			'fields': ('domain', 'notes'),
		}),
	)

	class Media:
		js = ['/static/js/admin_list_reorder.js',]

class MailUserAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'domain', 'mailbox_size', 'active')
	list_filter = ('domain',)

class MailQuotaAdmin(admin.ModelAdmin):
	pass

admin.site.register(MailDomain, MailDomainAdmin)
admin.site.register(MailUser, MailUserAdmin)
admin.site.register(MailQuota, MailQuotaAdmin)

admin.site.unregister(Group)
