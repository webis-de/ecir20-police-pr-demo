# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 22:18:18 2019

@author: Nina
"""
from elasticsearch import Elasticsearch
import csv
import webbrowser
import sys
from pprint import pprint
import urllib.request as urllib
from bs4 import BeautifulSoup
import re
from request import *
  
def search_for_police_articles(url):
  article = request(url)
  
  # return parsed article from csv if perfect match on url
  es = Elasticsearch(["http://betaweb023:9200"], timeout=30)
  es.cluster.health(wait_for_status='yellow', request_timeout=1)
  query = {"query": {"bool": {"should": [{"multi_match": {"query": str(article.title), "fields": ["title^2","body"] }},
  { "match": { "body": str(article.body) }},
  { "match": {"body":  str(article.date) } },
  {"multi_match": {"query": str(article.place), "fields": ["officeName","body^5","title"]}},
  { "range":{"timestamp" : {"time_zone": "+01:00", "gte": str(article.date2) + "-2w/w", "lte": str(article.date2)+ "8w/w" }}}]}}}
  result = es.search(index="ecir20-police-pr-demo", body=query, size=5)
  for hit in result['hits']['hits']:
    ret =  hit['_source']
    ret['_id'] = hit['_id']
    yield ret


def do_it(topic_id):
    file1 = open('results.txt','w')
    file2 = open("qrel.txt","w")
    print(topic_id)
    for topic in range(len(topic_id)):
        article_url = article_url_for_topic(topic)
        results = search_for_police_articles(article_url)
        r = 5
        j = 1
        for result in results:	
            print("%s %s" % (hit['_id'], hit['_index']))   
            file1.write(str(topic) + " Q0 \t"+ str(ret['_id']) + " "  + str(j) + " " + str(r) + "\t PPM_test_query \n")
            j = j+1
            r = r-1
            print(topic)
            print(ret['title'])
            print(ret['body'])
            print(ret['published'])
			#pprint(vars(hit['body']))
            relevant = input("How relevant is it? 0, 1 or 2?\t \n ")
            file2.write(str(topic_id[i]) + " 0 " + ret['_id'] + " " + str(relevant) + "\n")
            print("Your judment has been saved.\n ")
    file2.close()
    file1.close()	

do_it(['7_15'])
