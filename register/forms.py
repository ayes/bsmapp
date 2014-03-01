# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _

class RegistrationForm(UserCreationForm):
	def __init__(self, *args, **kwargs):
		super(RegistrationForm, self).__init__(*args, **kwargs)
		self.fields['username'].help_text = None
		self.fields['password2'].help_text = None
		self.fields['first_name'].required = True
		self.fields['last_name'].required = True
		self.fields['email'].required = True

	def clean_email(self):
		if User.objects.filter(email__iexact=self.cleaned_data['email']):
			raise forms.ValidationError(_("Alamat email ini sudah digunakan."))
		return self.cleaned_data['email']
	
	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email')