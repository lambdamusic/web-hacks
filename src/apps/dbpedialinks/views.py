#!/usr/bin/env python
# encoding: utf-8

from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import urlquote
from django.http import HttpResponse, HttpResponseNotFound
from django.db.models import Q

import string
from time import strftime
from collections import Counter, OrderedDict

import pyscigraph
import ontospy

from render_block import render_block_to_string
from .models import *


class OrderedCounter(Counter, OrderedDict):
    pass


def home(request):
    """
    landing page

    TIPS:

    In [14]: import string

    In [15]: string.letters
    Out[15]: 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

    In [16]: string.ascii_letters
    Out[16]: 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

    In [17]: string.ascii_lowercase
    Out[17]: 'abcdefghijklmnopqrstuvwxyz'

    In [18]: string.punctuation
    Out[18]: '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

    In [19]: string.printable
    Out[19]: '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'

    """

    letter = request.GET.get("letter", None)
    query = request.GET.get("query", None)

    alphabet = string.ascii_lowercase
    alphabet = alphabet + "*"

    punctuation_and_numbers = string.punctuation + "1234567890"

    entities = []

    if letter:
        if letter == "*":
            filterList = list(punctuation_and_numbers)
            query = Q()
            for x in filterList:
                query = query | Q(title__istartswith=x)
                entities = DBPediaEntity.objects.filter(query)
            query = None  # zero it not to interfere with template logic
        else:
            entities = DBPediaEntity.objects.filter(title__istartswith=letter)

    elif query:
        entities = DBPediaEntity.objects.filter(title__icontains=query)

    context = {
        'articlestot': SGDocument.objects.count(),
        'entitiestot': DBPediaEntity.objects.count(),
        'entities': entities,
        'alphabet': alphabet,
        'thisletter': letter,
        'query': query,
    }

    return render(request, 'dbpedialinks/home.html', context)


def entities(request, entity_id=None):
    """
    landing page + detail for entities
    """

    filters_id = request.GET.getlist("filters")

    if entity_id:

        subject = get_object_or_404(DBPediaEntity, pk=int(entity_id))
        filters = [subject]

        if filters_id:
            filters += [
                DBPediaEntity.objects.get(pk=int(x)) for x in filters_id
            ]
            print("===== Filters: ", str(filters))
            articles = SGDocument.objects.filter()
            for el in filters:
                articles = articles.filter(dbentities=el)

        else:
            # filters = []
            articles = subject.sgdocument_set.all()

        # CO-OCCURRING SUBJECTS

        if False:
            related = []

            for a in articles:
                related += a.dbentities.all()
            c = Counter(related)

            # sort manually as the OrderedDict was retuning weird results
            sorted_related = c.items()

            sorted_related = sorted(
                sorted_related, key=lambda t: (t[1], t[0].title), reverse=True)
        else:

            sorted_related = subject.related_subjects(
            )  # returns a list of tuples {subject: count}
            # top_20 = sorted_related.items()
            # top_20 = top_20[:20]
            # print(type(sorted_related), len(sorted_related))

        filters_minus_entity = [f for f in filters if f.id != subject.id]

        context = {
            'entity': subject,
            'filters': filters,
            'filters_minus_entity': filters_minus_entity,
            'articles': articles,
            'related_subjects': sorted_related,
            'related_subjects_graph': sorted_related[:20]
        }

    else:

        context = {'entity': None}

    return render(request, 'dbpedialinks/subject.html', context)


def ajax_scigraph(request):
    """
    Use SG API to get metadata

    eg http://scigraph.springernature.com/things/articles/0786393400bb0690ffbbc208884e5271
    """

    sg_id = request.GET.get("id", None)
    print("ID FOR SCIGRAPH === ", sg_id)

    cl = pyscigraph.SciGraphClient()
    e = cl.get_entity_from_id(uri=sg_id)

    if e:
        title = e.title
        doi = e.doi
        abstract = e.getValuesForProperty(
            "http://scigraph.springernature.com/ontologies/core/abstract")
        if abstract: abstract = abstract[0]

        context = {
            'article_id': sg_id,
            'title': title,
            'doi': doi,
            'abstract': abstract,
        }

        return_str = render_block_to_string(
            'dbpedialinks/snippet_ajax_article_info.html', 'article_info',
            context)

        return HttpResponse(return_str)

    else:
        return HttpResponse(
            "Sorry the request timed out - <a href='%s' target='_blank'>try on SciGraph?</a>"
            % sg_id)


def ajax_tags_info(request):
    """
    Get tag info via ajax

    eg http://scigraph.springernature.com/things/articles/0786393400bb0690ffbbc208884e5271
    """

    sg_id = request.GET.get("id", None)
    print("ID FOR SCIGRAPH === ", sg_id)

    article = get_object_or_404(SGDocument, uri=sg_id)

    context = {
        'tags': article.dbentities.all(),
    }

    return_str = render_block_to_string(
        'dbpedialinks/snippet_ajax_tag_info.html', 'tag_info', context)

    return HttpResponse(return_str)


def ajax_dbpedia_info(request):
    """
    Get dbpedia description info via ajax

    eg http://dbpedia.org/resource/Panicum_virgatum
    """

    dbpedia_id = request.GET.get("id", None)
    if "/page/" in dbpedia_id:
        dbpedia_id = dbpedia_id.replace("/page/", "resource/")
    print("ID FOR DBPedia === ", dbpedia_id)

    # load ontospy without generating schema info, but pull out URI entity
    o = ontospy.Ontospy(dbpedia_id, build_all=False)
    e = o.build_entity_from_uri(dbpedia_id)
    if e:
        desc = e.bestDescription()
    else:
        desc = "Entity description not found"

    # context = {
    #     'desc' : desc,
    # }

    # return_str = render_block_to_string('dbpedialinks/snippet_ajax_tag_info.html',
    #                                     'tag_info',
    #                                     context)

    return HttpResponse(desc)


def graph_test(request, entity_id=None):
    """
    landing page + detail for entities
    """

    filters_id = request.GET.getlist("filters")

    if entity_id:

        entity = get_object_or_404(DBPediaEntity, pk=int(entity_id))

        context = {
            'entity': entity,
            'related_subjects': entity.related_subjects(),
        }

    else:

        context = {'entity': None}

    return render(request, 'dbpedialinks/test/graph_test.html', context)


# ===========
# UNUSED
# ===========


def articles(request, article_id=None):
    """
    landing page + detail for articles
    """
    uri = request.GET.get("uri", None)

    if uri:

        # article = get_object_or_404(SGDocument, pk=int(article_id))
        article = get_object_or_404(SGDocument, uri=uri)

        context = {'article': article}

    else:
        context = {'article': None}

    return render(request, 'dbpedialinks/articles.html', context)
