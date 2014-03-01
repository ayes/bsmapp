from django.db import models
import datetime
from bsmapp.thumbs import ImageWithThumbsField

class PostManager(models.Manager):
    def judul_count(self, keyword):
        return self.filter(judul__icontains=keyword).count()

class Kategori(models.Model):
    kategori = models.CharField('Kategori', max_length = 100)
    
    def __unicode__(self):
        return self.kategori
    
    class Meta:
        db_table = 'blog_kategori'

class Post(models.Model):
	kategori = models.ForeignKey(Kategori, verbose_name = 'Kategori')
	tanggal = models.DateTimeField(auto_now_add=True)
	judul = models.CharField('Judul', max_length=100)
	penulis = models.CharField('Penulis', max_length=100)
	isi = models.TextField('Isi', max_length=100)
	label = models.CharField('Label', max_length=100)
	gambar = ImageWithThumbsField('Gambarnya', upload_to = 'blog-post', sizes=((250,180),))
	aktif = models.BooleanField('Ya/Tidak', help_text= 'Centang jika ingin mengaktifkan')
	views = models.IntegerField('Views')
	objects = PostManager()

	def __unicode__(self):
		return self.judul

	class Meta:
		db_table = 'blog_post'