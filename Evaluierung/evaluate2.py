# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 22:18:18 2019

@author: Nina
"""
from elasticsearch import Elasticsearch
import csv
import time
from article_requests import perfect_content_for_urls, parse_article_for_url, ParsedArticle
from run_files import run_file
from functools import lru_cache
from statistics import mean

def most_possible_complex_query_on_parsed_article(article):
    match_clauses = []

    if article.has_title():
        match_clauses += [{"multi_match": {"query": article.title(), "fields": ["title^2","body"] }}]

    if article.has_body():
        match_clauses += [{"match": {"body": article.body() }}]

    if article.has_date():
        match_clauses += [{"match": {"body":  article.date() }}]

    if article.has_place():
        match_clauses += [{"multi_match": {"query": article.place(), "fields": ["officeName","body","title"]}}]

    if article.has_date2():
        match_clauses += [{ "range":{"timestamp" : {"time_zone": "+01:00", "gte": article.date2() + "-2w/w", "lte": article.date2()+ "8w/w" }}}]

    return {"query": {"bool": {"should": match_clauses}}}

def complex_query(parsed_article):
    return most_possible_complex_query_on_parsed_article(parsed_article)


def title_query(parsed_article):
    return {"query": {"bool": {"should": [{"multi_match": {"query": parsed_article.title(), "fields": ["title^2","body"] }},]}}}

def full_text_query(parsed_article):
    return title_query(ParsedArticle({'title': parsed_article.title() + ' ' + parsed_article.body() }, ''))

def execute_query_for_article(query):
    es = Elasticsearch(["http://betaweb023:9200"], timeout=30, max_retries=10, retry_on_timeout=True)
    es.cluster.health(wait_for_status='yellow', request_timeout=1)
    result = es.search(index="ecir20-police-pr-demo", body=query, size=5)

    for hit in result['hits']['hits']:	
        yield hit

@lru_cache(maxsize=None)
def execute_query_url(article_url):
    parsed_article = parse_article_for_url(article_url)
    return [i for i in execute_query_for_article(most_possible_complex_query_on_parsed_article(parsed_article))]

def do_it(url, query_strategy):
    parsed_article = parse_article_for_url(url)
    for hit in execute_query_for_article(query_strategy(parsed_article)):
        yield hit['_id']
  
def test_it(query_strategy):
    topic_to_ranking = {}
    topics = perfect_content_for_urls()
    execution_times = []
    for url in topics:
        start = int(round(time.time() * 1000))
        topic_id = topics[url]['_id']
        topic_to_ranking[topic_id] = [i for i in do_it(url, query_strategy)]
        end =  int(round(time.time() * 1000))
        execution_times += [end-start]
    run_file('results/run' + query_strategy.__name__, topic_to_ranking, query_strategy.__name__)
    print('Mean exec-time for ' + query_strategy.__name__ + ': ' + str(mean(execution_times)))

if __name__ == '__main__':
    test_it(complex_query)
    test_it(full_text_query)
    test_it(title_query)

