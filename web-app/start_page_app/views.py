from django.shortcuts import render
from article_requests import parse_article_for_url, ParsedArticle
from evaluate2 import execute_query_url
from itertools import islice
from functools import lru_cache
from urllib.parse import unquote, quote
import json
import os

EXAMPLES = [{
    'id': 'ex1',
    'title': 'Murder in a cafe',
    'href': quote('https://web.archive.org/web/20190905203625/https://www.derwesten.de/staedte/duisburg/nettes-cafe-am-hafen-warum-wurde-ausgerechnet-im-vivo-eine-frau-getoetet-id210449711.html')
},
{
    'id': 'ex2',
    'title': 'Accident: Car + bycicle',
    'href': quote('https://web.archive.org/web/20190908183148/https://www.wz.de/nrw/krefeld/auto-faehrt-radlerin-an-schwer-verletzt_aid-25924297')
},
{
    'id': 'ex3',
    'title': 'Attack on bus driver',
    'href': quote('https://web.archive.org/web/20190909162230/https://www.wz.de/nrw/krefeld/erneuter-angriff-auf-busfahrer-in-krefeld_aid-25756075')
},{
    'id': 'ex4',
    'title': 'Dead animals in the circus',
    'href': quote('https://web.archive.org/web/20190823183325/https://www.veganblog.de/unterhaltung/19-tote-tiere-im-zirkus-wir-haben-anzeige-erstattet/')
},{
    'id': 'ex5',
    'title': 'Policeman mocked',
    'href': quote('https://web.archive.org/web/20190905200326/https://www.focus.de/regional/hessen/herborner-bahnhof-an-weihnachten-erstochen-linksradikale-verhoehnen-ermordeten-polizisten-im-netz_id_5177472.html')
}]


def add_shields_for_article(article):
    if article is None:
        return {}

    title_color = 'shield-green'
    if not article.has_title():
        title_color = 'shield-red'

    body_color = 'shield-green'
    if not article.has_body():
        body_color = 'shield-red'

    date_color = 'shield-green'
    if not article.has_date() and not article.has_date2():
        date_color = 'shield-red'
    elif not article.has_date():
        date_color = 'shield-yellow'

    loc_color = 'shield-green'
    if not article.has_place():
        loc_color = 'shield-red'

    return {
        'shields': {
            'titel_class': 'shield-title ' + title_color,
            'body_class': 'shield-body ' + body_color,
            'date_class': 'shield-date ' + date_color,
            'loc_class': 'shield-loc ' + loc_color,
        },
    }

def extract_article_from_request(request):
    article_url = request.GET.get('search', '')
    if not article_url:
        return None
    
    try:
        return parse_article_for_url(unquote(article_url))
    except Exception as e:
        return ParsedArticle({
            'title': '',
            'body': '',
            'place': '',
            'date': '',
        }, article_url)

def es_hit_to_serp_entry(hit):
    hit = hit['_source']
    words = hit['body'].split()

    return {
        'href':  hit['URL'],
        'title': hit['complete'],
        'location_link': hit['officeURL'],
        'location_name': hit['officeName'],
        'snippet': ' '.join(islice(words, 100)) + ('' if len(words) > 100 else '...'),
    }

@lru_cache(maxsize=None)
def persisted_ranking():
    f = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'start_page_app', 'persisted-examples.jsonl')
    with open(f, encoding='utf8') as json_file:
        return json.load(json_file)

def ranking_for_article(parsed_article):
    if parsed_article is None or not parsed_article.has_title():
        return None

    if parsed_article.url in persisted_ranking():
        result_list = persisted_ranking()[parsed_article.url]
    else:
        result_list = execute_query_url(parsed_article.url)

    return [es_hit_to_serp_entry(i) for i in islice(result_list, 10)]

def article_details(article):
    if article is None:
        return {}

    return {'content': {
        'title': article.title(),
        'date': article.date2() if article.has_date2() else article.date(),
        'place': article.place(),
        'body': article.body(),
    }}

def index(request):
    article = extract_article_from_request(request)
    context = {
        'news_article_url': '' if article is None else article.url,
        'example_list': EXAMPLES,
        'result_list': ranking_for_article(article),
    }
    context.update(add_shields_for_article(article))
    context.update(article_details(article))

    return render(request, 'start_page_app/index.html', context=context)

