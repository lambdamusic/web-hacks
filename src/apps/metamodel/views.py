#!/usr/bin/env python
# encoding: utf-8

from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import urlquote
from django.http import HttpResponse, HttpResponseNotFound

import os
from time import strftime
import time
import random

from .models import *


APP = "metamodel" # used to set the folder in /templates


def home(request):
	"""
	just an index of what's available  in /static for this app
	"""

	# print(static_templates_dir)
	keyword = request.GET.get("q", None)
	source = request.GET.get("s", None)
	product = request.GET.get("p", None)

	if keyword:
		data = Metafield.objects.filter(name__icontains=keyword).order_by("source", "name")
	
	elif source:
		data = Metafield.objects.filter(source=source).order_by("name")

	elif product:
		data = Metafield.objects.filter(implementation__platform=product).order_by("source", "name")

	else:
		data = Metafield.objects.all().order_by("source")


	sources_all = Metafield.objects.all().order_by("source").values_list("source", flat=True).distinct()

	platform_all = Implementation.objects.all().order_by("platform").values_list("platform", flat=True).distinct()

	context = {
		'q': keyword,
		's': source,
		'p': product,
		'fields': data,
		'sources_all': sources_all,
		'platform_all': platform_all,
	}

	return render(request, APP + '/home.html', context)



from functools import reduce
import operator
from django.db.models import Q



def detail(request, field_id):
	"""
	detail page for fields 
	"""

	# print(static_templates_dir)
	val = request.GET.get("q", None)

	field = get_object_or_404(Metafield, pk=int(field_id))


	contains = field.name.split("_")
	similar = Metafield.objects.filter(reduce(operator.or_, (Q(name__icontains=x) for x in contains)))

	context = {
		'q': val,
		'field': field,
		'similar': similar,
		'is_admin_user': request.user.is_superuser
	}

	return render(request, APP + '/detail_field.html', context)




# ===========
# unused
# ===========


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

