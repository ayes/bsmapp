from django.db import models

TARGET_CHOICES =  (
    ('_self', '_self'),
    ('_blank', '_blank'),
    )

class SoftProfile(models.Model):
	nama = models.CharField('Nama', max_length = 100)

	def __unicode__(self):
		return self.nama

	class Meta:
		db_table = 'portal_soft_profile'

class KategoriPortFolio(models.Model):
	kategori = models.CharField('Kategori', max_length = 100)

	def __unicode__(self):
		return self.kategori

	class Meta:
		db_table = 'portal_kategori_portfolio'

class PortFolio(models.Model):
	kategori = models.ForeignKey(KategoriPortFolio, verbose_name = 'Kategori')
	judul = models.CharField('Judul', max_length = 100)
	deskripsi = models.TextField('Deskripsi', max_length = 200)
	website = models.URLField()
	target_url = models.CharField('Target URL', max_length = 10, choices=TARGET_CHOICES, default='_self')
	gambar_kecil = models.ImageField(u'Gambar Kecil', upload_to = 'portal-portfolio')
	gambar_besar = models.ImageField(u'Gambar Besar', upload_to = 'portal-portfolio')

	def __unicode__(self):
		return self.judul

	class Meta:
		db_table = 'portal_portfolio'

class Download(models.Model):
	count = models.PositiveIntegerField('Counter', default = 0)

	class Meta:
		db_table = 'portal_download'