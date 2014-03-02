from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from userdash.models import UserBalance
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect, Http404
from acp.models import *
from userdash.forms import *
from bsmapp.settings import PAYPAL_RECEIVER_EMAIL
from paypal.standard.forms import PayPalPaymentsForm
from django.core.urlresolvers import reverse
import random

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
		active = request.POST.get('active', False)
		
		if (len(username) == 0) or (len(domain) == 0) or (len(password) == 0):
			return edit_user_email(request, u'Anda harus mengisi semua bidang')
		dom = MailDomain.objects.get(pk=domain)
		usermail = MailUser.objects.get(id=idmail)
		usermail.username = username
		usermail.domain = dom
		usermail.password= password
		usermail.active = active
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
		domain = request.POST.get('domain', domain)
		password = request.POST.get('password', '')
		quota = request.POST.get('quota', quota)
		active = request.POST.get('active', '')
	
	return render_to_response('userdash_add_user_email.html',
		{
		'success': success,
		'error': error,
		'berhasil': berhasil,
		'username': username,
		'domain': domain,
		'password': password,
		'quota': quota,
		'active': active,
		'user_balance':get_balance(request)
		}, RequestContext(request))

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
		active = request.POST.get('active', False)
		
		if (len(username) == 0) or (len(domain) == 0) or (len(password) == 0) or (len(quota) == 0):
			return add_user_email(request, u'Anda harus mengisi semua bidang')

		balance = get_balance(request)
		price = MailQuota.objects.get(pk=quota)

		if balance.balance < price.price:
			return add_user_email(request, u'Maaf deposit anda tidak mencukupi')

		balance.balance -= price.price
		balance.save()

		dom = MailDomain.objects.get(pk=domain)
		qta = MailQuota.objects.get(pk=quota)
		usermail = MailUser(username=username, domain=dom, password=password, quota=qta, active=active)
		usermail.save()
		return HttpResponseRedirect('/dashboard-cust/user-email')
	else:
		return HttpResponseRedirect('/dashboard-cust/add-user-email')

from django.views.decorators.csrf import csrf_exempt, csrf_protect

@login_required()
@csrf_exempt
def kelola_pembayaran(request):

	return render_to_response('userdash_kelola_pembayaran.html', {'user_balance':get_balance(request)}, RequestContext(request))

def generate_code():
	result = ''
	for i in range(0, 4):
		result += random.choice('0123456789')
	
	return result


@login_required()
@csrf_exempt
def deposit_paypal(request):

    paypal_dict = {
        "business": PAYPAL_RECEIVER_EMAIL,
        "amount": "1.00",
        "item_name": "name of the item",
        "invoice": generate_code(),
        "notify_url": "http://bsmsite.com" + reverse('paypal-ipn'),
        "return_url": "http://bsmsite.com/dashboard-cust/kelola-pembayaran/",
        "cancel_return": "http://bsmsite.com/your-cancel-location/",

    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {'form': form}
    return render_to_response("userdash_paypal.html", context)

