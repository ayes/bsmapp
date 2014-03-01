# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

def home_page(request):
	return HttpResponseRedirect('http://mail.bsmsite.com/admin')
