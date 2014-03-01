from django.shortcuts import render
from register.forms import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from portal.views import get_kategori, get_style
from django.http import HttpResponse, HttpResponseRedirect, Http404
from userdash.models import UserBalance

def register(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/dashboard-cust');
	else:
		if request.method == 'GET':
			form = RegistrationForm()
			return render_to_response('portal_register_page.html',
				{
					'form': form,
					'kategori_list':get_kategori(request),
					'style':get_style(),
				}, RequestContext(request))
		else:
			form = RegistrationForm(request.POST)
			if form.is_valid():
				new_user = form.save()
				balance = UserBalance(user_id=new_user.id,)
				balance.save()
				return HttpResponseRedirect('/')
			else:
				return render_to_response('portal_register_page.html',
					{
						'form': form,
						'kategori_list':get_kategori(request),
						'style':get_style(),
					}, RequestContext(request))
