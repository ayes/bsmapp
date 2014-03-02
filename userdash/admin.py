from django.contrib import admin
from userdash.models import *

class UserBalanceAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'balance')

admin.site.register(UserBalance, UserBalanceAdmin)
