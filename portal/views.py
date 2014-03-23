from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from portal.models import *
from blog.models import *
from blog.views import get_kategori
from django.contrib import auth
import random
from userdash.models import UserBalance

def get_style():
	return random.choice(['orange.css', 'purple.css', 'lblue.css', 'red.css', 'green.css', 'blue.css'])

def main(request):
	try:
		portfolio = PortFolio.objects.order_by('?')[:5]
	except:
		portfolio = {}

	return render_to_response('portal_main.html',
		{
			'kategori_list':get_kategori(),
			'style':get_style(),
			'portfolio':portfolio,
		}, RequestContext(request))

def fazashop(request):
	return render_to_response('portal_product_fazashop.html',
		{
			'kategori_list':get_kategori(),
			'style':get_style(),
		}, RequestContext(request))

def bsmretailpos(request):
	return render_to_response('portal_product_bsmretailpos.html',
		{
			'kategori_list':get_kategori(),
			'style':get_style(),
		}, RequestContext(request))

def webdevelopment(request):
	return render_to_response('portal_service_web_development.html',
		{
			'kategori_list':get_kategori(),
			'style':get_style(),
		}, RequestContext(request))

def mailserver(request):
	return render_to_response('portal_service_mail_server.html',
		{
			'kategori_list':get_kategori(),
			'style':get_style(),
		}, RequestContext(request))

def radiostreaming(request):
	return render_to_response('portal_service_radio_streaming.html',
		{
			'kategori_list':get_kategori(),
			'style':get_style(),
		}, RequestContext(request))

def labs_zamanda(request):
	return render_to_response('portal_labs_zamanda.html',
		{
			'kategori_list':get_kategori(),
			'style':get_style(),
		}, RequestContext(request))

def labs_siak(request):
	return render_to_response('portal_labs_siak.html',
		{
			'kategori_list':get_kategori(),
			'style':get_style(),
		}, RequestContext(request))

def contact_us(request):
	return render_to_response('portal_contact_us.html',
		{
			'kategori_list':get_kategori(),
			'style':get_style(),
		}, RequestContext(request))

def about_us(request):
	return render_to_response('portal_about_us.html',
		{
			'kategori_list':get_kategori(),
			'style':get_style(),
		}, RequestContext(request))

def portfolio(request):
	try:
		kategori = KategoriPortFolio.objects.all()
	except:
		kategori = {}

	try:
		portfolio = PortFolio.objects.all()
	except:
		portfolio = {}

	return render_to_response('portal_portfolio.html',
		{
			'kategori':kategori,
			'portfolio':portfolio,
			'kategori_list':get_kategori(),
			'style':get_style(),
		}, RequestContext(request))

def search(request):
	errors = []
	try:
		q
	except:
		q = ''
		errors.append('ketik pencarian anda.')

	if 'q' in request.GET:
		q = request.GET['q']
		if not q:
			errors.append('ketik pencarian anda.')
		elif len(q) > 200:
			errors.append('Silahkan masukan tidak lebih dari 200 huruf pada pencarian.')
		else:
			blog = Post.objects.filter(judul__icontains=q)
			return render(request, 'portal_search_results.html',
				{'blog': blog, 'query': q, 'kategori_list':get_kategori(), 'style':get_style()})
	return render(request, 'portal_search_results.html',
		{'errors': errors, 'query': q, 'kategori_list':get_kategori(request), 'style':get_style()})

def login(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/dashboard-cust');
	if request.method == 'GET':
		return render_to_response('portal_login_page.html',
			{
				'kategori_list':get_kategori(),
				'style':get_style(),
			}, RequestContext(request))
	else:
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		user = auth.authenticate(username = username, password = password)
		try:
			balance = UserBalance.objects.get(user_id=user.pk)
		except:
			balance = None

		if user is not None and balance is not None and user.is_active:
			auth.login(request, user)
			return HttpResponseRedirect('/dashboard-cust')
		else:
			return render_to_response('portal_login_page.html', 
				{
					'error': u'Password login tidak valid',
					'kategori_list':get_kategori(),
					'style':get_style(),
				}, RequestContext(request))