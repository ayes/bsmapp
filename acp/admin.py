# -*- coding: utf-8 -*-

from django import forms
from django.contrib import admin
#from django.contrib.auth.models import Group
from acp.models import *

class MultiDBModelAdmin(admin.ModelAdmin):
    # A handy constant for the name of the alternate database.
    using = 'mail'

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(MultiDBModelAdmin, self).queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(MultiDBModelAdmin, self).formfield_for_foreignkey(db_field, request=request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(MultiDBModelAdmin, self).formfield_for_manytomany(db_field, request=request, using=self.using, **kwargs)

class MailDomainAdmin(MultiDBModelAdmin):
	list_display = ('__unicode__', 'notes', 'position')
	list_editable = ('position',)

	fieldsets = (
		('', {
			'fields': ('domain', 'notes'),
		}),
	)

	class Media:
		js = ['/static/js/admin_list_reorder.js',]

class MailUserAdmin(MultiDBModelAdmin):
	list_display = ('__unicode__', 'domain', 'mailbox_size', 'active')
	list_filter = ('domain',)

class MailQuotaAdmin(admin.ModelAdmin):
	pass

#admin.site.register(MailDomain, MultiDBModelAdmin)

admin.site.register(MailDomain, MailDomainAdmin)
admin.site.register(MailUser, MailUserAdmin)
admin.site.register(MailQuota, MultiDBModelAdmin)

#admin.site.unregister(Group)
