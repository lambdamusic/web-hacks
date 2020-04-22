#!/usr/bin/env python
# encoding: utf-8

from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import urlquote
from django.http import HttpResponse, HttpResponseNotFound

import os
from time import strftime
import time
import random

from render_block import render_block_to_string
from .models import *


APP = "html_fun" # used to set the folder in /templates


def straight_to_template(request, filename):
	"""
	do something where you can pass an html file name and it'll just rended that template
	"""
	# NOTE: filename never has the extension so we add it manually
	# ... PS urls.py regex could be updated if needed

	val = request.GET.get("val", None)
	template = APP + '/static/%s.html' % str(filename)

	context = {
		'query': val,
	}

	return render(request, template, context)


def home(request):
	"""
	just an index of what's available  in /static for this app
	"""

	here = os.path.dirname(os.path.realpath(__file__))
	static_templates_dir = here + "/templates/"+ APP + "/static/"
	static_templates = os.listdir(static_templates_dir)

	# print(static_templates_dir)
	val = request.GET.get("val", None)

	context = {
		'query': val,
		'static_templates': static_templates,
	}

	return render(request, APP + '/home.html', context)


# ===========
# dynamic experiments
# ===========




def fun(request):
	"words of increasing size"
	u = ""
	n = 10

	def create_style(n, text):
		s = "<span style=\"color: sienna; font-size:" + n.__str__() + "\">" + text + "</span>"
		return s

	for x in range(50):
		for i in ["uno ", "due ", "tre ", "quattro "]:
			n += 1
			u += create_style(n, i)

	return HttpResponse(u)




def colors(request):
	u = ""
	colors_set = ['red', 'green', 'blue', 'yellow', 'lavender']
	for x in range(1550):
		wid = random.randrange(1, 140)	  
		u += createPattern(random.choice(colors_set), wid)
	u = "<div style=\"float:left; border-left: 1px solid white; width: 500px;\"><p style=\"display: -moz-grid-group;\"> " + u + "</p></div>"
	return HttpResponse(u)	  

def createPattern(col, wid):
	s = "<a style=\"background: " + col + "; width: " + wid.__str__() + "%; display: block; float: left;\"><span style=\"visibility: hidden; display: -moz-grid-group;\">x</span></a><span style=\"visibility: hidden; display: -moz-grid-group;\">v</span>"
	return s
	
	# I can't manage to recreate what's happening in the perseus project!!!






LOCATION = 'london'

#In [13]: time.gmtime()
#Out[13]: (2010, 4, 28, 7, 16, 6, 2, 118, 0)


def clock(request):
	t = time.gmtime()
	u1 = ""
	u2 = ""
	u3 = ""

	def random_message():
		# add more messages on demand, or get them online	 
		msg = ["..e qua tutto bene", "..and I am still sleepy", "..and the date? who knows the date?" ]
		if random.random() > .6 :
			return random.choice(msg)
		else:
			return ""

	for x in range(1,25):
		if x == t[3]:
			u1 += "<p style=\"color: red;\">%s</p>" % (x)
		else:
			u1 += "<p style=\"color: grey;\">%s</p>" % (x)
	for x in range(1,25):
		if x == t[3]:
			u2 += "<p><span style=\"font-size: 12px; color: black;\">Hi there. <br />It is %s:%s in London %s</span></p>" % (t[3], t[4], random_message() )
		else:
			u2 += "<p style=\"color: white;\">%s</p>" % (x)

	context = {	'stuff1' : u1 , 
				'stuff2' : u2 , 
				'stuff3' : u3  }

	return render(request, APP + '/clock.html', context)





def typer(request):
	"""
	Test for typer.js
	"""
	context = {'stuff1' : None }
	return render(request, APP + '/typer.html', context)





# here we're randomly picking animated gifs from a folder, and displaying them on a page
# there are many more gifs we can experiment with!

def visuals(request):
	""" random animated gifs """
	listof_choices = _getGifFilesList()
	random_gif = random.choice(listof_choices)
	tot = 800
	x = ""
	if True:
		random_gif = random.choice(listof_choices)
		tot = 800
		x = ""
		for n in range(tot):
			x += """<img src="%s" />"""	 % random_gif
		return HttpResponse(x)

	if False: 
		# legacy: needs to be updated
		if random.random() > .5:
			listof_choices = [f for f in os.listdir(gifs_root) if f.startswith("combination_square_002")]	
			tot = 400
		else:
			listof_choices = [f for f in os.listdir(gifs_root) if f.startswith("combination_square")]	
			tot = 30



def _getGifFilesList():
	""" returns a list of gifs from the static folder - as ready-to-use URLs """
	from settings import STATIC_URL, STATICFILES_DIRS
	print(STATICFILES_DIRS[0])
	LOCAL_GIF_FOLDER = STATICFILES_DIRS[0] + '/custom/html_fun/gif/'
	print(LOCAL_GIF_FOLDER)
	gifs_root = LOCAL_GIF_FOLDER
	listof_choices = ["%scustom/html_fun/gif/%s" % (STATIC_URL, f) for f in os.listdir(gifs_root) if not f.startswith(".")]
	return listof_choices





