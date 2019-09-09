#!/usr/bin/env python
# encoding: utf-8

#
from django.shortcuts import render
import requests
import json
import sys
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

#
QUERY = """
    search publications in concepts for "{}" 
    return publications[basics+concepts+doi+times_cited] sort by times_cited limit 100 
    """



def home(request):
    """
    home page (and possibly the only one)
    """
    # topics1, topics2 = batches(TOPICS, 2)
    # res, tot, q = None, None, None
    searchterm = request.GET.get("query", "")
    # restrict = request.GET.get("restrict", "")
    # country = request.GET.get("country", "")

    if searchterm:
        q = QUERY.format(searchterm)
        print(q)
        res = do_query(q)
        print(res.keys())
        # res = json.loads(res)
        tot = res['_stats']['total_count']

    context = {
        'res': res,
        'tot': tot,
        'query': searchterm,
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
