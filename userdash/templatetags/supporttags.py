from django import template
from support.models import *

register = template.Library()

@register.filter(name='replaysupport')
def replaysupport(ticket_id, arg):
	replay =  ReplaySupport.objects.filter(ticket_id=ticket_id).latest('id')
	if (arg == 'post_date'):
		return replay.post_date
	elif (arg == 'user'):
		return replay.user
	else:
		return None

@register.filter(name='create_date_support')
def create_date_support(ticket_id):
	replay =  ReplaySupport.objects.filter(ticket_id=ticket_id).order_by('id')[0]
	return replay.post_date

@register.filter
def status(q):
    for choice in STATUS_CHOICES:
        if choice[0] == q:
            return choice[1]
    return ''