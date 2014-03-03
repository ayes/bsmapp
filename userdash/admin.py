from django.contrib import admin
from userdash.models import *

class UserBalanceAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'balance')

class CashBookAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'code', 'invoice', 'tanggal', 'item', 'masuk', 'keluar', 'balance')

admin.site.register(UserBalance, UserBalanceAdmin)
admin.site.register(CashBook, CashBookAdmin)