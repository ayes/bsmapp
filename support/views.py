from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from userdash.views import get_balance
from django.template import RequestContext
from support.forms import *
from django.http import HttpResponseRedirect, Http404

@login_required()
def support(request):
	try:
		ticket = TicketSupport.objects.filter(user=request.user).exclude(status=3)
	except:
		ticket = {}
	try:
		ticket_closed = TicketSupport.objects.filter(user=request.user, status=3)
	except:
		ticket_closed = {}
	return render_to_response('support_ticket.html', {'user_balance':get_balance(request), 'ticket':ticket, 'ticket_closed':ticket_closed, 'menu_support':'active'}, RequestContext(request))

@login_required()
def add_support_ticket(request):
	if request.method == 'GET':
		form = SupportForm()
		form_ask = ReplaySupportForm()
		return render_to_response('support_add_ticket.html', {'user_balance':get_balance(request), 'form':form, 'form_ask':form_ask, 'menu_support':'active'}, RequestContext(request))
	else:
		form = SupportForm(request.POST)
		form_ask = ReplaySupportForm(request.POST)
		if form.is_valid():
			instance = TicketSupport(user=request.user, type_support=TypeSupport.objects.get(pk=request.POST.get('type_support')), subject=request.POST.get('subject'))
			instance.save()
			instance_ask = ReplaySupport(ticket=TicketSupport.objects.get(pk=instance.pk), user=request.user, body=request.POST.get('body'))
			instance_ask.save()
			return HttpResponseRedirect('/dashboard-cust/support')
		else:
			return render_to_response('support_add_ticket.html', {'user_balance':get_balance(request), 'form':form, 'form_ask':form_ask, 'menu_support':'active'}, RequestContext(request))

@login_required()
def view_support_ticket(request, ticket_id):
	if request.method == 'GET':
		try:
			ticket = TicketSupport.objects.get(pk=ticket_id, user=request.user)
		except:
			raise Http404

		try:
			support = ReplaySupport.objects.select_related('ticket').filter(ticket=ticket_id, ticket__user=request.user).order_by('-pk')
		except:
			support = {}

		form = ReplaySupportForm()
		return render_to_response('support_view_ticket.html', {'user_balance':get_balance(request), 'support':support, 'form':form, 'ticket':ticket, 'menu_support':'active'}, RequestContext(request))
	else:
		form = ReplaySupportForm(request.POST)
		if form.is_valid():
			instance = ReplaySupport(user=request.user, ticket=TicketSupport.objects.get(pk=request.POST.get('idsupport')), body=request.POST.get('body'))
			instance.save()
			return HttpResponseRedirect('/dashboard-cust/view-support-ticket/' + request.POST.get('idsupport'))
		else:
			return render_to_response('support_view_ticket.html', {'user_balance':get_balance(request), 'support':support, 'form':form, 'menu_support':'active'}, RequestContext(request))

@login_required()
def close_support_ticket(request, ticket_id):
	try:
		ticket = TicketSupport.objects.get(pk=ticket_id, user=request.user)
	except:
		raise Http404
	ticket.status = 3
	ticket.save()
	return HttpResponseRedirect('/dashboard-cust/support')