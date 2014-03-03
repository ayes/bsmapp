from django.db import models
from django.contrib.auth.models import User
from paypal.standard.ipn.signals import payment_was_successful

class UserBalance(models.Model):
	user = models.ForeignKey(User, unique=True)
	balance = models.DecimalField(max_digits=18, decimal_places=2, verbose_name='balance', default=0.00)

	def __unicode__(self):
		return self.user.username

	class Meta:
		db_table = 'userdash_user_balance'

class CashBook(models.Model):
	user = models.ForeignKey(User)
	code = models.CharField('Code', max_length=3)
	invoice = models.CharField('Invoice', max_length=127)
	tanggal = models.DateTimeField(auto_now_add=True)
	item = models.CharField('Item', max_length=255)
	masuk = models.DecimalField(max_digits=18, decimal_places=2, verbose_name='Masuk', default=0.00)
	keluar = models.DecimalField(max_digits=18, decimal_places=2, verbose_name='Keluar', default=0.00)
	balance = models.DecimalField(max_digits=18, decimal_places=2, verbose_name='balance', default=0.00)

	def __unicode__(self):
		return self.user.username

	class Meta:
		db_table = 'userdash_cash_book'

def show_me_the_money(sender, **kwargs):
	ipn_obj = sender
	balance = UserBalance.objects.get(user_id=ipn_obj.item_number)
	if ipn_obj.payment_status == "Completed":
		balance.balance += ipn_obj.mc_gross
		balance.save()

		cash_balance = balance.balance
		get_user = User.objects.get(pk=ipn_obj.item_number)
		cashbook = CashBook(user_id=get_user.id, code='IN', invoice=invoice, item=ipn_obj.item_name, masuk=ipn_obj.mc_gross, balance=cash_balance)
		cashbook.save()

payment_was_successful.connect(show_me_the_money)