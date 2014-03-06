from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from userdash.views import get_balance
from django.template import RequestContext
from support.forms import *
from django.http import HttpResponseRedirect, Http404

@login_required()
def support(request):
	try:
		support = TicketSupport.objects.filter(user=request.user).order_by('-pk')
	except:
		support = {}

	return render_to_response('support_ticket.html', {'user_balance':get_balance(request), 'support':support}, RequestContext(request))

@login_required()
def add_support_ticket(request):
	if request.method == 'GET':
		form = SupportForm()
		return render_to_response('support_add_ticket.html', {'user_balance':get_balance(request), 'form':form}, RequestContext(request))
	else:
		form = SupportForm(request.POST)
		if form.is_valid():
			instance = TicketSupport(user=request.user, type_support=TypeSupport.objects.get(pk=request.POST.get('type_support')), subject=request.POST.get('subject'), body=request.POST.get('body'))
			instance.save()
			return HttpResponseRedirect('/dashboard-cust/support')
		else:
			return render_to_response('support_add_ticket.html', {'user_balance':get_balance(request), 'form':form}, RequestContext(request))

@login_required()
def view_support_ticket(request, ticket_id):
	try:
		support = TicketSupport.objects.get(pk=ticket_id, user=request.user)
	except:
		raise Http404

	return render_to_response('support_view_ticket.html', {'user_balance':get_balance(request), 'support':support}, RequestContext(request))