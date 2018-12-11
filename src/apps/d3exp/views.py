#!/usr/bin/env python
# encoding: utf-8

from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import urlquote
from django.http import HttpResponse, HttpResponseNotFound
from django.db.models import Q

from time import strftime

from render_block import render_block_to_string
from .models import *


def get_template(request, filename):
    """
    do something where you can pass an html file name and it'll just rended that template
    """

    val = request.GET.get("val", None)
    template = 'd3s/%s.html' % str(filename)

    context = {
        'query': val,
    }

    return render(request, template, context)


def home(request):
    """
    """

    val = request.GET.get("val", None)

    context = {
        'query': val,
    }

    return render(request, 'd3s/home.html', context)
