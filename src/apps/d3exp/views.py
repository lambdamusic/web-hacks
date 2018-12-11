#!/usr/bin/env python
# encoding: utf-8

from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import urlquote
from django.http import HttpResponse, HttpResponseNotFound

import os
from time import strftime

from render_block import render_block_to_string
from .models import *


def straight_to_template(request, filename):
    """
    do something where you can pass an html file name and it'll just rended that template
    """
    # NOTE: filename never has the extension so we add it manually
    # ... PS urls.py regex could be updated if needed

    val = request.GET.get("val", None)
    template = 'd3exp/static/%s.html' % str(filename)

    context = {
        'query': val,
    }

    return render(request, template, context)


def home(request):
    """
    just an index of what's available (dynamic if possible)
    """

    here = os.path.dirname(os.path.realpath(__file__))
    static_templates_dir = here + "/templates/d3exp/static/"
    static_templates = os.listdir(static_templates_dir)

    # print(static_templates_dir)
    val = request.GET.get("val", None)

    context = {
        'query': val,
        'static_templates': static_templates,
    }

    return render(request, 'd3exp/home.html', context)
