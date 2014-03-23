from django.contrib import admin
from portal.models import *

class SoftProfileAdmin(admin.ModelAdmin):
	pass

class KategoriPortFolioAdmin(admin.ModelAdmin):
	pass

class PortFolioAdmin(admin.ModelAdmin):
	pass

admin.site.register(SoftProfile, SoftProfileAdmin)
admin.site.register(KategoriPortFolio, KategoriPortFolioAdmin)
admin.site.register(PortFolio, PortFolioAdmin)