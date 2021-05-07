from article_requests import parse_article_for_url
from blaulicht_client import search
from run_files import run_file
import xml.etree.ElementTree as ET
import os

def topics_file():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Topics', 'Topics.xml')

def all_persistent_urls():
    for topic in ET.parse(topics_file()).getroot():
        yield topic.findall('persistentUrl')[0].text

if __name__ == '__main__':
    topic_to_ranking = {}
    for topic in ET.parse(topics_file()).getroot():
        topic_id = topic.findall('topicId')[0].text
        url = topic.findall('persistentUrl')[0].text
        print(topic_id + '->' + url +'\n\n')
        parsedDocument = parse_article_for_url(url) 
        print(parsedDocument.title())
        topic_to_ranking[topic_id] = search(parsedDocument.title())
        print(topic_to_ranking[topic_id])
        print('\n\n')

    run_file('results/runBlaulichtTitleSearch', topic_to_ranking, 'blaulichtTitleSearch')

