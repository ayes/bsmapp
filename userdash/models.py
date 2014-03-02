from django.db import models
from django.contrib.auth.models import User

class UserBalance(models.Model):
	user = models.ForeignKey(User, unique=True)
	balance = models.DecimalField(max_digits=18, decimal_places=2, verbose_name='balance', default=0.00)

	def __unicode__(self):
		return self.user.username

	class Meta:
		db_table = 'userdash_user_balance'
