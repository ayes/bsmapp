# -*- coding: utf-8 -*-

from django.db import models
from django.forms import ValidationError
from django.contrib.auth.models import User
import re

class Orderable(models.Model):
	position = models.IntegerField(u'Position', blank = True)

	def save(self, *args, **kwargs):
		if self.position is None:
			try:
				last = self.objects.order_by('-position')[0]
				self.position = last.position + 1
			except:
				self.position = 0
		
		return super(Orderable, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.address

	class Meta:
		abstract = True
		ordering = ('position',)

class MailDomain(Orderable):
	user = models.ForeignKey(User)
	domain = models.CharField(u'Nama Domain', max_length = 64, help_text = 'contoh: bsmsite.com', unique = True)
	notes = models.CharField(u'Keterangan', max_length = 1024)

	def __unicode__(self):
		return self.domain

	class Meta:
		db_table = 'domains'
		verbose_name = 'mail domain'
		verbose_name_plural = 'mail domains'
		ordering = ('position',)

class MailQuota(models.Model):
	quota = models.IntegerField('Quota, megabytes', help_text = u'User quota in megabytes, 0 means unlimited')
	title = models.CharField('Quota name', help_text = 'Example: 100 megabytes, for staff', max_length = 255)
	price = models.DecimalField(max_digits=18, decimal_places=2, verbose_name='Price', default=0.00)

	def __unicode__(self):
		return self.title

	class Meta:
		db_table = 'quotas'
		verbose_name = 'Mail quota'
		verbose_name_plural = 'Mail quotas'

def validate_username(username):
	if re.match(r'^[a-z_]+$', username) is None:
		raise ValidationError('Wrong username format. Please use only latin letters (a-z) and the underscore (_)')

class MailUser(models.Model):
	def __unicode__(self):
		return self.username

	def mailbox_size(self):
		return self.quota.title

	username = models.CharField('Username', max_length = 64, help_text = 'Left part (before @ sign) of the e-mail address', validators = [validate_username])
	domain = models.ForeignKey(MailDomain, verbose_name = 'Domain')
	password = models.CharField('Password', max_length = 32, help_text = 'Used to connect through POP, IMAP and SMTP')
	quota = models.ForeignKey(MailQuota, verbose_name = 'Mailbox size')
 	active = models.BooleanField('Access', default=True, help_text = 'Disabling the user’s access does not destroy his mailbox')
 	date_begin = models.DateTimeField(auto_now_add=True)
 	date_expired = models.DateTimeField('Date Expired')

	class Meta:
		db_table = 'users'
		verbose_name = 'mail user'
		verbose_name_plural = 'mail users'
		ordering = ('username',)

def validate_alias_source(source_name):
	if re.match(r'^[a-z_]+$', source_name) is None:
		raise ValidationError('Wrong alias source format. Please use only latin letters (a-z) and the underscore (_)')

class MailAlias(models.Model):
	source_username = models.CharField('Source username', max_length = 64, help_text = 'Left part (before @ sign) of the alias', validators = [validate_alias_source])
	source_domain = models.ForeignKey(MailDomain, verbose_name = 'Source domain', help_text = 'Source domain (right part of the alias)')
	destination = models.ForeignKey(MailUser, verbose_name = 'Destination mailbox', help_text = 'Mails will be delivered to this mailbox')
	active = models.BooleanField('Access', default = True, help_text = 'Activity flag')
 	date_begin = models.DateTimeField(auto_now_add = True)
 	date_expired = models.DateTimeField('Date Expired')

 	def __unicode__(self):
 		return self.source_address()

 	def destination_domain(self):
 		return self.destination.domain

 	def source_address(self):
 		return "%s@%s" % (self.source_username, self.source_domain)

 	def destination_address(self):
 		return "%s@%s" % (self.destination.username, self.destination.domain)

 	class Meta:
 		db_table = 'aliases'
 		verbose_name = 'mail alias'
 		verbose_name_plural = 'mail aliases'
