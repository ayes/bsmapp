from django import forms
from acp.models import *
from django.contrib.auth.models import User

class MailUserForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(MailUserForm, self).__init__(*args, **kwargs)

	class Meta:
		model = MailUser
		fields = ('username', 'domain', 'password', 'quota', 'active')

class UserForm(forms.ModelForm):   
    class Meta:
        model = User
        fields = ('first_name', 'last_name' ,'email')
    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)