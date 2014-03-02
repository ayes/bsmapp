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

def show_me_the_money(sender, **kwargs):
	ipn_obj = sender
	balance = UserBalance.objects.get(user_id=ipn_obj.item_number)
	if ipn_obj.payment_status == "Completed":
		balance.balance += 1
		balance.save()

payment_was_successful.connect(show_me_the_money)