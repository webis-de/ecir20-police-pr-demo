from blaulicht_client import extract_article_urls_from_serp, extract_pagination_links_from_serp
import sys
from unittest import TestCase

class TestExtractionOfLinks(TestCase):

    def test_extraction_of_article_links_for_linux_in_2014(self):
        serp = self.load_resource('search-for-linux-in-2014')
        expected = ['https://www.presseportal.de/blaulicht/pm/12726/2848577']
        actual = extract_article_urls_from_serp(serp)

        self.assertListEqual(expected, actual)

    def test_extraction_of_pagination_links_for_linux_in_2014(self):
        serp = self.load_resource('search-for-linux-in-2014')
        actual = extract_pagination_links_from_serp(serp)

        self.assertListEqual([], actual)

    def test_extraction_of_pagination_links_for_all_articles_at_2018_12_31(self):
        serp = self.load_resource('all-articles-at-2018-12-31')
        expected = [
                'https://www.presseportal.de/blaulicht?startDate=2018-12-31&endDate=2018-12-31&sort=asc',
                'https://www.presseportal.de/blaulicht/27?startDate=2018-12-31&endDate=2018-12-31&sort=asc',
                'https://www.presseportal.de/blaulicht/54?startDate=2018-12-31&endDate=2018-12-31&sort=asc',
                'https://www.presseportal.de/blaulicht/81?startDate=2018-12-31&endDate=2018-12-31&sort=asc',
                'https://www.presseportal.de/blaulicht/108?startDate=2018-12-31&endDate=2018-12-31&sort=asc',
                'https://www.presseportal.de/blaulicht/135?startDate=2018-12-31&endDate=2018-12-31&sort=asc',
                'https://www.presseportal.de/blaulicht/162?startDate=2018-12-31&endDate=2018-12-31&sort=asc'
        ]
        actual = extract_pagination_links_from_serp(serp)

        self.assertListEqual(expected, actual)

    def load_resource(self, resource):
        with open('test/resources/' + resource + '.html') as f:
            return f.read()
