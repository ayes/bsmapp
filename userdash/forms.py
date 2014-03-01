from django import forms
from acp.models import *

class MailUserForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(MailUserForm, self).__init__(*args, **kwargs)

	class Meta:
		model = MailUser
		fields = ('username', 'domain', 'password', 'quota', 'active')