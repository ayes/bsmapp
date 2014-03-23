from django.shortcuts import render
from blog.models import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404
import random

def get_style():
	return random.choice(['orange.css', 'purple.css', 'lblue.css', 'red.css', 'green.css', 'blue.css'])

def get_post_lainnya(request):
	try:
		pl = Post.objects.order_by('?')[:5]
	except:
		pl = {}

	return pl

def get_kategori():
	try:
		kategori = Kategori.objects.all()
	except:
		kategori = {}

	return kategori

def blog_category(request, kategori_id):
	try:
		blog_list = Post.objects.filter(kategori_id = kategori_id)
	except:
		raise Http404

	return render_to_response('blog_main.html',
		{
			'blog_list':blog_list,
			'kategori_list':get_kategori(),
			'pl_list':get_post_lainnya(request),
			'style':get_style()
		}, RequestContext(request))

def blog_read(request, post_id):
	try:
		blog_list = Post.objects.get(id = post_id)
	except:
		raise Http404

	return render_to_response('blog_read.html',
		{
			'bl':blog_list,
			'kategori_list':get_kategori(),
			'pl_list':get_post_lainnya(request),
			'style':get_style()
		}, RequestContext(request))

def blog(request):
	blog_list = Post.objects.all()

	return render_to_response('blog_main.html',
		{
			'blog_list':blog_list,
			'kategori_list':get_kategori(),
			'pl_list':get_post_lainnya(request),
			'style':get_style()
		}, RequestContext(request))