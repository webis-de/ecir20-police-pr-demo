from bs4 import BeautifulSoup
import argparse
from urllib.parse import quote
from datetime import date
from dateutil.relativedelta import relativedelta
import requests
import time
import os

def search(query):
    query = quote(query)
    response = requests.get('https://www.presseportal.de/blaulicht/suche/' + query).content.decode("utf-8")
    return extract_ranking_from_serp(response)

def extract_ranking_from_serp(serp):
    return [article_url_to_id(i) for i in extract_article_urls_from_serp(serp)]

def extract_article_urls_from_serp(serp):
    return ['https://www.presseportal.de' + i.get('data-url') for i in BeautifulSoup(serp, features="html.parser")\
         .select('article[class="news"][data-url]')]

def extract_pagination_links_from_serp(serp):
    return ['https://www.presseportal.de' + i.get('data-url').replace('@', '') for i in BeautifulSoup(serp, features="html.parser")\
         .select('span[class="btn pagination-link"][data-url]')]

def article_url_to_id(article):
    return article.split('/blaulicht/pm/')[1].replace('/', '-')

def fail_if_dir_exists(directory):
    if os.path.exists(directory):
        raise ValueError('Directory already exists.... ' + directory)

def crawl_all_sites(url, directory):
    sites_visited = set([url])
    frontier = set([url])

    while frontier:
        url = frontier.pop()
        with open(directory + '/request-hash-' + str(hash(url)), 'w') as f:
            print('Visit: ' + url)
            response = requests.get(url).content.decode("utf-8")
            f.write(response)
            sites_visited.update([url])
            frontier.update([i for i in extract_pagination_links_from_serp(response) if i not in sites_visited])
            sites_visited.update(frontier)
            time.sleep(5)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Blaulicht-Client: Parse + load pages from https://www.presseportal.de/blaulicht/')
    parser.add_argument('--year', type=int, required=True)
    parser.add_argument('--month', type=int, required=True)
    args = parser.parse_args()

    current_date = date(args.year, args.month, 1)
    end_date = current_date + relativedelta(months=+1)

    if not os.path.exists(str(args.year)):
        os.mkdir(str(args.year))
    fail_if_dir_exists(str(args.year) + '/' + str(args.month))
    os.mkdir(str(args.year) + '/' + str(args.month))

    while current_date < end_date:
        print('Crawl at : ' + str(current_date))
        directory = str(args.year) + '/' + str(args.month) + '/' + str(current_date.day)
        os.mkdir(directory)
        crawl_all_sites(
                url = 'https://www.presseportal.de/blaulicht/?startDate='+ str(current_date) +'&endDate='+ str(current_date) +'&sort=asc',
                directory = directory
        )
        current_date = current_date + relativedelta(days=+1)

    print('Done ;)')
