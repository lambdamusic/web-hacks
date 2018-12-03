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

TOPICS = [
    {
        'name': 'Undernourishment',
        'color': 'btn-primary'
    },
    {
        'name': 'Food insecurity',
        'color': 'btn-info'
    },
    {
        'name': 'Stunting',
        'color': 'btn-success'
    },
    {
        'name': 'Malnutrition',
        'color': 'btn-danger'
    },
    {
        'name': 'Agricultural productivity',
        'color': 'btn-warning'
    },
    {
        'name': 'Sustainable agriculture',
        'color': 'btn-info'
    },
    {
        'name': 'Genetic diversity',
        'color': 'btn-primary'
    },
    {
        'name': 'Expenditure flows',
        'color': 'btn-warning'
    },
    {
        'name': 'Trade restrictions',
        'color': 'btn-success'
    },
    {
        'name': 'Food commodity markets',
        'color': 'btn-danger'
    },
]

# SDG => Sustainable Development Goals
# MDG => Millennium Development Goals

#
QUERY = """
    search publications in full_data for "(%s AND SDG) OR (%s AND MDG)"
where year in [2000:2018] and type="article" %s
    return publications [basics-issue-volume-pages+doi+times_cited] sort by times_cited
    return in "facets"
    funders[name + country_name] as "entity_funder" 
    return in "facets" research_orgs[all]
    return in "facets" researchers[all]   
    """

RESTRICT_CLAUSE = """ and journal.title~"Nature" """


def home(request):
    """
    home page (and possibly the only one)
    """
    topics1, topics2 = batches(TOPICS, 2)
    res, tot = None, None
    searchterm = request.GET.get("s", "")
    restrict = request.GET.get("restrict", "")

    if searchterm:
        res = do_query(searchterm, restrict)
        # print type(res)
        # print res.keys()
        # res = json.loads(res)
        tot = res['_stats']['total_count']

    context = {
        'topics1': topics1,
        'topics2': topics2,
        'search_topic': searchterm,
        'restrict': restrict,
        'res': res,
        'tot': tot
    }

    return render(request, 'zerohunger/home.html', context)


def do_query(s, restrict):
    """
    """

    login = {'username': DIMENSIONS_USR, 'password': DIMENSIONS_PSW}

    if restrict:
        r = RESTRICT_CLAUSE
    else:
        r = ""

    query = QUERY % (s, s, r)

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
    if False:  # debug
        print_json(res)
    return res
