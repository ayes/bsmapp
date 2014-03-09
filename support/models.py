from django.db import models
from django.contrib.auth.models import User

STATUS_CHOICES =  (
    (1, 'Baru'),
    (2, 'Dijawab'),
    (3, 'Ditutup'),
    )

class TypeSupport(models.Model):
	type_support = models.CharField(u'Jenis Bantuan', max_length = 100, unique = True)
	description = models.CharField(u'Keterangan', max_length = 1024)

	def __unicode__(self):
		return self.type_support

	class Meta:
		db_table = 'support_type'

class TicketSupport(models.Model):
	user = models.ForeignKey(User)
	type_support = models.ForeignKey(TypeSupport, verbose_name = 'Jenis Bantuan')
	status = models.IntegerField('Status', max_length = 1, choices=STATUS_CHOICES, default=1)
	subject = models.CharField(u'Judul', max_length = 100)

	def __unicode__(self):
		return self.subject

	class Meta:
		db_table = 'support_ticket'

class ReplaySupport(models.Model):
	ticket = models.ForeignKey(TicketSupport, verbose_name = 'Ticket')
	user = models.ForeignKey(User)
	body = models.TextField(u'Komentar', max_length=1024)
	post_date = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return str(self.ticket.pk)

	class Meta:
		db_table = 'support_replay'
