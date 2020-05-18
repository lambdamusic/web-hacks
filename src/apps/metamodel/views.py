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


APP = "metamodel" # used to set the folder in /templates


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

	# print(static_templates_dir)
	val = request.GET.get("q", None)

	if val:
		data = Metafield.objects.filter(name__icontains=val).order_by("source")
	else:
		data = Metafield.objects.all().order_by("source")

	context = {
		'q': val,
		'fields': data,
	}

	return render(request, APP + '/home.html', context)




def detail(request, field_id):
	"""
	detail page for fields 
	"""

	# print(static_templates_dir)
	val = request.GET.get("q", None)

	field = get_object_or_404(Metafield, pk=int(field_id))

	similar = Metafield.objects.filter(name__icontains=field.name).order_by("source")

	context = {
		'q': val,
		'field': field,
		'similar': similar,
	}

	return render(request, APP + '/detail_field.html', context)




# ===========
# dynamic views
# ===========

# @TODO

