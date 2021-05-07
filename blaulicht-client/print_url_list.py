from blaulicht_client import extract_article_urls_from_serp
import os
from sys import stderr

all_urls = set([])

for directory in ['2017', '2018', '2019']:
    if os.path.exists(directory):
        for month in os.listdir(directory):
            for day in os.listdir(directory + '/' + month):
                urls_in_day = set([])
                for f in os.listdir(directory + '/' + month + '/' + day):
                    with open(directory + '/' + month +'/' + day + '/' + f, 'r') as html_file:
                        urls_in_day.update(extract_article_urls_from_serp(html_file.read()))
                print(directory + '-' + month + '-' + day +': ' + str(len(urls_in_day)), file=stderr)
                all_urls.update(urls_in_day)

all_urls = sorted([i for i in all_urls])
for url in all_urls:
    print(url)
