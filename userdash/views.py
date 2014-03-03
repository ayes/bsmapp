from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from userdash.models import *
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect, Http404
from acp.models import *
from userdash.forms import *
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
from django.core.urlresolvers import reverse
import random
from django.views.decorators.http import require_POST
from datetime import datetime, timedelta

def get_balance(request):
	user = request.user
	return UserBalance.objects.get(user_id=user.pk)

@login_required()
def dashboard_cust(request):
	return render_to_response('userdash_dashboard_user.html', {'user_balance':get_balance(request)}, RequestContext(request))

@login_required()
def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/')

@login_required()
def domain_email(request):
	user = request.user

	try:
		domain = MailDomain.objects.filter(user_id=user.pk)
	except:
		domain = {}

	return render_to_response('userdash_domain_email.html', {'user_balance':get_balance(request), 'domain':domain}, RequestContext(request))

@login_required()
def user_email(request):
	user = request.user

	try:
		usermail = MailUser.objects.select_related('domain').filter(domain__user_id=user.pk)
	except:
		usermail = {}

	return render_to_response('userdash_user_email.html', {'user_balance':get_balance(request), 'usermail':usermail}, RequestContext(request))

@login_required()
def edit_user_email(request, post_id):
	user = request.user

	try:
		usermail = MailUser.objects.select_related('domain').get(id=post_id, domain__user_id=user.pk)
	except:
		raise Http404

	try:
		domain =  MailDomain.objects.filter(user_id=user.pk)
	except MailDomain.DoesNotExist:
		raise Http404

	return render_to_response('userdash_edit_user_email.html',
		{
			'user_balance':get_balance(request),
			'usermail':usermail,
			'domain':domain
		}, RequestContext(request))

@login_required()
@require_POST
def update_user_email(request):
	user = request.user

	try:
		domain =  MailDomain.objects.filter(user_id=user.pk)
	except MailDomain.DoesNotExist:
		raise Http404

	if request.method == 'POST':
		idmail = request.POST.get('idmail', '')
		username = request.POST.get('username', '')
		domain = request.POST.get('domain', '')
		password = request.POST.get('password', '')
		
		if (len(username) == 0) or (len(domain) == 0) or (len(password) == 0):
			return edit_user_email(request, u'Anda harus mengisi semua bidang')

		dom = MailDomain.objects.get(pk=domain)
		usermail = MailUser.objects.get(id=idmail)
		usermail.username = username
		usermail.domain = dom
		usermail.password= password
		usermail.save()
		return HttpResponseRedirect('/dashboard-cust/user-email')
	else:
		return HttpResponseRedirect('/dashboard-cust/edit-user-email')

@login_required()
def add_user_email(request, error = None, berhasil = None, success = False):
	user = request.user

	try:
		domain =  MailDomain.objects.filter(user_id=user.pk)
	except MailDomain.DoesNotExist:
		raise Http404

	try:
		quota = MailQuota.objects.all()
	except MailQuota.DoesNotExist:
		raise Http404

	if not success:
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')

	return render_to_response('userdash_add_user_email.html',
		{
		'success': success,
		'error': error,
		'berhasil': berhasil,
		'username': username,
		'domain': domain,
		'password': password,
		'quota': quota,
		'user_balance':get_balance(request)
		}, RequestContext(request))

def generate_code():
	result = ''
	for i in range(0, 10):
		result += random.choice('0123456789')
	
	return result

@login_required()
@require_POST
def create_user_email(request):
	user = request.user

	try:
		domain =  MailDomain.objects.filter(user_id=user.pk)
	except MailDomain.DoesNotExist:
		raise Http404

	try:
		quota = MailQuota.objects.all()
	except MailQuota.DoesNotExist:
		raise Http404

	if request.method == 'POST':
		username = request.POST.get('username', '')
		domain = request.POST.get('domain', '')
		password = request.POST.get('password', '')
		quota = request.POST.get('quota', '')
		
		if (len(username) == 0) or (len(domain) == 0) or (len(password) == 0) or (len(quota) == 0):
			return add_user_email(request, u'Anda harus mengisi semua bidang')

		try:
			user_identic = MailUser.objects.select_related('domain').get(username=username, domain__id=domain)
		except:
			user_identic = None

		if user_identic is not None:
			return add_user_email(request, u'username tersebut sudah ada')

		balance = get_balance(request)
		price = MailQuota.objects.get(pk=quota)

		if balance.balance < price.price:
			return add_user_email(request, error=u'Maaf deposit anda tidak mencukupi')
		parts = ('CM', user.pk, generate_code())
		no_invoice = "-".join(str(s) for s in parts if s is not None)
		balance.balance -= price.price
		balance.save()

		dom = MailDomain.objects.get(pk=domain)
		qta = MailQuota.objects.get(pk=quota)
		parts = (username, dom, qta)
		create_email = "-".join(str(s) for s in parts if s is not None)
		waktu = datetime.now() + timedelta(days=30)
		usermail = MailUser(username=username, domain=dom, password=password, quota=qta, date_expired=waktu)
		usermail.save()

		cash_balance = balance.balance
		cashbook = CashBook(user_id=user.pk, code='OUT', invoice=no_invoice, item=create_email, keluar=price.price, balance=cash_balance)
		cashbook.save()
		return HttpResponseRedirect('/dashboard-cust/user-email')
	else:
		return HttpResponseRedirect('/dashboard-cust/add-user-email')

@login_required()
@csrf_exempt
def cash_book(request):
	user = request.user

	try:
		cash_book =  CashBook.objects.filter(user_id=user.pk)
	except:
		cash_book = {}

	return render_to_response('userdash_cash_book.html', {'user_balance':get_balance(request), 'cash_book':cash_book}, RequestContext(request))

from django.views.decorators.csrf import csrf_exempt, csrf_protect

@login_required()
def customer_profile(request, error = None, berhasil = None):
	if request.method == 'GET':
		form = UserForm(instance=request.user)
		return render_to_response('userdash_edit_customer_profile.html', {'form': form, 'error':error, 'user_balance':get_balance(request)}, RequestContext(request))
	elif request.method == 'POST':
		first_name = request.POST.get('first_name', '')
		last_name = request.POST.get('last_name', '')
		email = request.POST.get('email', '')

		userprofile = User.objects.get(id=request.user.id)
		userprofile.first_name = first_name
		userprofile.last_name = last_name
		userprofile.email= email
		userprofile.save()
		return HttpResponseRedirect('/dashboard-cust/customer-profile')
		
@login_required()
@csrf_exempt
def kelola_pembayaran(request):

	return render_to_response('userdash_kelola_pembayaran.html', {'user_balance':get_balance(request)}, RequestContext(request))

@login_required()
@require_POST
@csrf_exempt
def deposit_paypal(request):
	user = request.user
	parts = ('PP', user.pk, generate_code())
	no_invoice = "-".join(str(s) for s in parts if s is not None)

	if request.method == 'POST':
		deposit = request.POST.get('deposit', '')

	paypal_dict = {
		"business": settings.PAYPAL_RECEIVER_EMAIL,
		"amount": deposit,
		"item_name": "Paypal Deposit",
		"item_number": user.id,
		"invoice": no_invoice,
		"notify_url": "http://bsmsite.com" + reverse('paypal-ipn'),
		"return_url": "http://bsmsite.com/dashboard-cust/cash-book/",
		"cancel_return": "http://bsmsite.com/your-cancel-location/",
	}

	form = PayPalPaymentsForm(initial=paypal_dict)
	context = {'form': form, 'depo':deposit, 'user_balance':get_balance(request), 'no_invoice':no_invoice}
	return render_to_response("userdash_paypal.html", context)