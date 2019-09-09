#!/usr/bin/env python
# encoding: utf-8

#
from django.shortcuts import render
import requests
import json
import sys
from collections import Counter
#
from libs.myutils.lists import batches
from libs.myutils.myutils import print_json
#
try:
    from settings import DIMENSIONS_USR, DIMENSIONS_PSW
except:
    print("SETTINGS NOT FOUND: DIMENSIONS_USR, DIMENSIONS_PSW")
    raise

DEBUG_MODE = False  # set to True to print out useful info in the console


QUERY = """
    search publications in concepts for "{}" 
    return publications[basics+concepts+doi+times_cited] sort by times_cited limit 100 
    """



def home(request):
    """
    home page (and possibly the only one)
    """
    URL_AND_SYMBOL = "AND"
    res, tot, q, related_concepts = None, None, None, {}
    searchquery = request.GET.get("query", "")
    if searchquery.endswith(URL_AND_SYMBOL):
        searchquery = searchquery[:-3]
    search_concepts = searchquery.split(URL_AND_SYMBOL)

    # print(searchquery)
    # print(search_concepts)

    def search_terms_join(s):
        "from a 'AND' list make a proper concepts search query"
        bits = s.strip().split(URL_AND_SYMBOL)
        return " AND ".join(["\\\"{}\\\"".format(x) for x in bits if x])

    def count_concepts(res):
        c = []
        for p in res['publications']:
            c += p['concepts']
        return Counter(c)


    if searchquery:
        q = QUERY.format(search_terms_join(searchquery))
        print(q)
        res = do_query(q)
        
        try:
            tot = res['_stats']['total_count']
            print("Results ==>", tot)
        except:
            print(res.keys())
        
        all_concepts = count_concepts(res)
        related_concepts  = all_concepts.most_common(400)
        # print(related_concepts)

    context = {
        'res': res,
        'tot': tot,
        'searchquery': searchquery,
        'search_concepts': search_concepts,
        # https://docs.python.org/3/library/collections.html#collections.Counter.most_common
        'related_concepts': related_concepts,
    }

    return render(request, 'dslconcepts/search.html', context)



def do_query(query):
    """
    """

    login = {'username': DIMENSIONS_USR, 'password': DIMENSIONS_PSW}

    #   Send credentials to login url to retrieve token. Raise
    #   an error, if the return code indicates a problem.
    #   Please use the URL of the system you'd like to access the API
    #   in the example below.
    resp = requests.post('https://app.dimensions.ai/api/auth.json', json=login)
    resp.raise_for_status()

    #   Create http header using the generated token.
    headers = {'Authorization': "JWT " + resp.json()['token']}

    #   Execute DSL query.
    resp = requests.post(
        'https://app.dimensions.ai/api/dsl.json', data=query, headers=headers)

    #   Display raw result
    res = resp.json()
    if DEBUG_MODE:  # DEBUG
        print(query)
        print_json(res)
    return res
