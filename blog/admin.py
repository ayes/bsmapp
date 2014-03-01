from django.contrib import admin
from blog.models import *

class KategoriAdmin(admin.ModelAdmin):
	pass

class PostAdmin(admin.ModelAdmin):
	
	class Media:
		js = ['/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js', '/static/grappelli/tinymce_setup/tinymce_setup.js',]

admin.site.register(Kategori, KategoriAdmin)
admin.site.register(Post, PostAdmin)
