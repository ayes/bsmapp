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
from dns.resolver import Resolver

def get_balance(request):
	return UserBalance.objects.get(user=request.user)

@login_required()
def dashboard_cust(request):
	return render_to_response('userdash_dashboard_user.html', { 'user_balance':get_balance(request), 'menu_home':'active' }, RequestContext(request))

@login_required()
def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/')

@login_required()
def domain_email(request):
	try:
		domain = MailDomain.objects.filter(user=request.user)
	except:
		domain = {}

	return render_to_response('userdash_domain_email.html', {'user_balance':get_balance(request), 'domain':domain, 'menu_email':'active'}, RequestContext(request))

@login_required()
def add_domain_email(request):
	if request.method == 'GET':
		form = MailDomainForm()
		return render_to_response('userdash_add_domain_email.html', {'user_balance':get_balance(request), 'form':form, 'menu_email':'active'}, RequestContext(request))
	else:
		form = MailDomainForm(request.POST)
		if form.is_valid():
			try:

				local_resolver = Resolver()
				name_servers = local_resolver.query(request.POST.get('domain'), 'NS')

				uncached_resolver = Resolver(configure = False)
				for i in name_servers:
					try:
						authentic_address = local_resolver.query(str(i), 'A')
						resolver.nameservers.append(str(authentic_address[0]))
					except: # one of the servers was broken?
						pass

				address = uncached_resolver.query(request.POST.get('domain'), 'MX')
			except:
				return HttpResponseRedirect('/dashboard-cust/error-domain-email')

			try:
				exchanger = str(address[0])
				if not exchanger.endswidth('bsmsite.com.'): # NOTE: srv.bsmsite.com and mail.bsmsite.com are both valid
					return HttpResponseRedirect('/dashboard-cust/error-domain-email')
			except:
				return HttpResponseRedirect('/dashboard-cust/error-domain-email')

			instance = MailDomain(user=request.user, domain=request.POST.get('domain'), notes=request.POST.get('notes'))
			instance.save()
			return HttpResponseRedirect('/dashboard-cust/domain-email')
		else:
			return render_to_response('userdash_add_domain_email.html', {'user_balance':get_balance(request), 'form':form, 'menu_email':'active'}, RequestContext(request))

@login_required()
def delete_domain_email(request, domain_id):
	try:
		domain = MailDomain.objects.get(id=domain_id, user=request.user)
	except:
		raise Http404
	if request.method == 'GET':
		form = DomainNotesEditForm(instance=domain)
		return render_to_response('userdash_delete_domain_email.html', {'user_balance':get_balance(request), 'form':form, 'domain':domain, 'menu_email':'active'}, RequestContext(request))
	else:
		raise Http404

@login_required()
@require_POST
def delete_confirm_domain_email(request):
	try:
		domain = MailDomain.objects.get(id=request.POST.get('domain_id'), user=request.user)
	except:
		raise Http404
	
	domain.delete()
	return HttpResponseRedirect('/dashboard-cust/domain-email')

@login_required()
def edit_domain_email(request, domain_id):
	try:
		domain = MailDomain.objects.get(id=domain_id, user=request.user)
	except:
		raise Http404
	if request.method == 'GET':
		form = DomainNotesEditForm(instance=domain)
		return render_to_response('userdash_edit_domain_email.html', {'user_balance':get_balance(request), 'form':form, 'domain':domain, 'menu_email':'active'}, RequestContext(request))
	else:
		form = DomainNotesEditForm(request.POST, instance=domain)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard-cust/domain-email')
        else:
        	return render_to_response('userdash_edit_domain_email.html', {'user_balance':get_balance(request), 'form':form, 'domain':domain, 'menu_email':'active'}, RequestContext(request))

@login_required()
def error_domain_email(request):
		return render_to_response('userdash_error_domain_email.html', {'user_balance':get_balance(request), 'menu_email':'active'}, RequestContext(request))

@login_required()
def user_email(request):
	try:
		usermail = MailUser.objects.select_related('domain').filter(domain__user=request.user)
	except:
		usermail = {}

	return render_to_response('userdash_user_email.html', {'user_balance':get_balance(request), 'usermail':usermail, 'menu_email':'active'}, RequestContext(request))

@login_required()
def edit_user_email(request, error = None, post_id = None):
	try:
		usermail = MailUser.objects.select_related('domain').get(id=post_id, domain__user=request.user)
	except:
		raise Http404

	return render_to_response('userdash_edit_user_email.html',
		{
			'user_balance':get_balance(request),
			'usermail':usermail,
			'error':error,
			'menu_email':'active'
		}, RequestContext(request))

@login_required()
@require_POST
def update_user_email(request):
	try:
		domain =  MailDomain.objects.filter(user=request.user)
	except MailDomain.DoesNotExist:
		raise Http404

	if request.method == 'POST':
		idmail = request.POST.get('idmail', '')
		password = request.POST.get('password', '')
		
		if len(password) == 0:
			return edit_user_email(request, u'Anda harus mengisi password')

		usermail = MailUser.objects.get(id=idmail)
		usermail.password= password
		usermail.save()
		return HttpResponseRedirect('/dashboard-cust/user-email')
	else:
		return HttpResponseRedirect('/dashboard-cust/edit-user-email')

@login_required()
def add_user_email(request, error = None, berhasil = None, success = False):
	try:
		domain =  MailDomain.objects.filter(user=request.user)
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
		'user_balance':get_balance(request),
		'menu_email':'active'
		}, RequestContext(request))

@login_required()
def delete_user_email(request, usermail_id):
	try:
		usermail = MailUser.objects.select_related('domain').get(id=usermail_id, domain__user=request.user)
	except:
		raise Http404

	if request.method == 'GET':
		return render_to_response('userdash_delete_user_email.html', {'user_balance':get_balance(request), 'usermail':usermail, 'menu_email':'active'}, RequestContext(request))
	else:
		raise Http404

@login_required()
@require_POST
def delete_confirm_user_email(request):
	try:
		usermail = MailUser.objects.select_related('domain').get(id=request.POST.get('usermail_id'), domain__user=request.user)
	except:
		raise Http404
	
	usermail.delete()
	return HttpResponseRedirect('/dashboard-cust/user-email')

def generate_code():
	result = ''
	for i in range(0, 10):
		result += random.choice('0123456789')
	
	return result

@login_required()
@require_POST
def create_user_email(request):
	try:
		domain =  MailDomain.objects.filter(user=request.user)
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
		parts = ('CM', request.user.pk, generate_code())
		no_invoice = "-".join(str(s) for s in parts if s is not None)
		balance.balance -= price.price
		balance.save()

		dom = MailDomain.objects.get(pk=domain)
		qta = MailQuota.objects.get(pk=quota)
		parts = (username, dom, qta)
		create_email = "-".join(str(s) for s in parts if s is not None)
		waktu = datetime.now() + timedelta(days=365)
		usermail = MailUser(username=username, domain=dom, password=password, quota=qta, date_expired=waktu)
		usermail.save()

		cash_balance = balance.balance
		cashbook = CashBook(user=request.user, code='OUT', invoice=no_invoice, item=create_email, keluar=price.price, balance=cash_balance)
		cashbook.save()
		return HttpResponseRedirect('/dashboard-cust/user-email')
	else:
		return HttpResponseRedirect('/dashboard-cust/add-user-email')

from django.views.decorators.csrf import csrf_exempt, csrf_protect

@login_required()
@csrf_exempt
def cash_book(request):
	try:
		cash_book =  CashBook.objects.filter(user=request.user).order_by('-id')
	except:
		cash_book = {}

	return render_to_response('userdash_cash_book.html', {'user_balance':get_balance(request), 'cash_book':cash_book, 'menu_report':'active'}, RequestContext(request))

@login_required()
def customer_profile(request, error = None, berhasil = None):
	if request.method == 'GET':
		form = UserForm(instance=request.user)
		return render_to_response('userdash_edit_customer_profile.html', {'form': form, 'error':error, 'user_balance':get_balance(request), 'menu_setting':'active'}, RequestContext(request))
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
def management_payment(request):
	return render_to_response('userdash_management_payment.html', {'user_balance':get_balance(request), 'menu_payment':'active'}, RequestContext(request))

@login_required()
@csrf_exempt
def cancel_deposit_paypal(request):
		return render_to_response('userdash_cancel_deposit_paypal.html', {'user_balance':get_balance(request), 'menu_payment':'active'}, RequestContext(request))

@login_required()
@require_POST
@csrf_exempt
def deposit_paypal(request):
	parts = ('PP', request.user.id, generate_code())
	no_invoice = "-".join(str(s) for s in parts if s is not None)

	if request.method == 'POST':
		deposit = request.POST.get('deposit', '')

	paypal_dict = {
		"business": settings.PAYPAL_RECEIVER_EMAIL,
		"amount": deposit,
		"item_name": "Paypal Deposit",
		"item_number": request.user.id,
		"invoice": no_invoice,
		"notify_url": "http://"+ settings.DOMAIN_MY_SITE + reverse('paypal-ipn'),
		"return_url": "http://"+ settings.DOMAIN_MY_SITE +"/dashboard-cust/cash-book/",
		"cancel_return": "http://"+ settings.DOMAIN_MY_SITE +"/dashboard-cust/cancel-deposit-paypal",
	}

	form = PayPalPaymentsForm(initial=paypal_dict)
	context = {'form': form, 'depo':deposit, 'user_balance':get_balance(request), 'no_invoice':no_invoice, 'menu_payment':'active'}
	return render_to_response("userdash_paypal.html", context)

from django.contrib.auth.views import password_change as builtin_password_change
from django.contrib.auth.views import password_change_done as builtin_password_change_done

def password_change(request, **kwargs):
	return builtin_password_change(request, extra_context = {'user_balance': get_balance(request)}, **kwargs)

def password_change_done(request, **kwargs):
	return builtin_password_change_done(request, extra_context = {'user_balance': get_balance(request)}, **kwargs)
