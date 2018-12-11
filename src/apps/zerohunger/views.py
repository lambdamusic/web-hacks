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
    search publications in full_data for "(%s AND SDG) OR (%s AND MDG)%s%s"
    where year in [2000:2018] 
    return publications [basics-issue-volume-pages+doi+times_cited] sort by times_cited
    return in "facets"
    funders[name + country_name] as "entity_funder" 
    return in "facets" research_orgs[all]
    return in "facets" researchers[all]   
    """

COUNTRY_CLAUSE = " AND %s "
RESTRICT_CLAUSE = """ AND (doi:10.1038* OR doi:10.1007* OR doi:10.1186*) """

DOI_STEMS = {
    '10.1013':
    'Nature Publishing Group',
    '10.1038':
    'Nature Publishing Group',
    '10.1057':
    'Nature Publishing Group - Macmillan Publishers',
    '10.1251':
    'Springer (Biological Procedures Online)',
    '10.1186':
    'Springer (Biomed Central Ltd.)',
    '10.4076':
    'Springer (Cases Network, Ltd.)',
    '10.1114':
    'Springer (Kluwer Academic Publishers - Biomedical Engineering Society',
    '10.1023':
    'Springer (Kluwer Academic Publishers)',
    '10.5819':
    'Springer - (backfiles)',
    '10.1361':
    'Springer - ASM International',
    '10.1379':
    'Springer - Cell Stress Society International',
    '10.1065':
    'Springer - Ecomed Publishers',
    '10.1381':
    'Springer - FD Communications',
    '10.7603':
    'Springer - Global Science Journals',
    '10.1385':
    'Springer - Humana Press',
    '10.4098':
    'Springer - Mammal Research Institute',
    '10.3758':
    'Springer - Psychonomic Society',
    '10.1617':
    'Springer - RILEM Publishing',
    '10.5052':
    'Springer - Real Academia de Ciencias Exactas, Fisicas y Naturales',
    '10.1245':
    'Springer - Society of Surgical Oncology',
    '10.4333':
    'Springer - The Korean Society of Pharmaceutical Sciences and Technology',
    '10.1365':
    'Springer Fachmedien Wiesbaden GmbH',
    '10.1891':
    'Springer Publishing Company',
    '10.1140':
    'Springer-Verlag',
    '10.1007':
    'Springer-Verlag',
}

RESTRICT_CLAUSE = "AND (%s) " % " OR ".join(["doi:%s*" % x for x in DOI_STEMS])

print(RESTRICT_CLAUSE)


def home(request):
    """
    home page (and possibly the only one)
    """
    topics1, topics2 = batches(TOPICS, 2)
    res, tot, q = None, None, None
    searchterm = request.GET.get("s", "")
    restrict = request.GET.get("restrict", "")
    country = request.GET.get("country", "")

    if searchterm:
        q = construct_query(searchterm, restrict, country)
        res = do_query(q)
        # print type(res)
        # print res.keys()
        # res = json.loads(res)
        tot = res['_stats']['total_count']

    context = {
        'topics1': topics1,
        'topics2': topics2,
        'search_topic': searchterm,
        'restrict': restrict,
        'country': country,
        'query': q,
        'res': res,
        'tot': tot
    }

    return render(request, 'zerohunger/search.html', context)


def construct_query(s, restrict, country):
    if restrict:
        r = RESTRICT_CLAUSE
    else:
        r = ""

    if country:
        c = COUNTRY_CLAUSE % country
    else:
        c = ""

    query = QUERY % (s, s, c, r)
    return query


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
    if False:  # debug
        print_json(res)
    return res
