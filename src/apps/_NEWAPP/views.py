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


APP = "_NEWAPP" # used to set the folder in /templates


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
# dynamic views
# ===========

# @TODO

