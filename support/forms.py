from django import forms
from support.models import *

class SupportForm(forms.ModelForm):
	class Meta:
		model = TicketSupport
		fields = ('type_support', 'subject' ,'body')