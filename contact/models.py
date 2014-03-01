from django.db import models

class Contact(models.Model):
	nama = models.CharField('Nama', max_length=100)
	email = models.EmailField('Email', max_length=100)
	nohp = models.CharField('No HP', max_length=100)
	komentar = models.TextField('Komentar')

	def __unicode__(self):
		return self.nama

	class Meta:
		db_table = 'contact_contactform'
