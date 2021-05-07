from blaulicht_client import extract_ranking_from_serp
import sys
from unittest import TestCase

class TestParsingOfSerps(TestCase):
    def test_parsing_of_serp_for_gameboy(self):
        serp = self.load_resource('search-for-gameboy')
        expected = ['30127-3911308', '68442-3217351', '65841-3009540', '8-2655836', '4969-1155515', '4969-958842', '19027-926440', '4970-895048', '8-858499', '6013-738580', '4969-729287', '12726-689693', '12726-681745', '8-662391', '6013-660747', '8-504098', '8-361808', '12726-334179', '6013-141812']
        actual = extract_ranking_from_serp(serp)

        self.assertListEqual(expected, actual)

    def test_parsing_of_serp_for_linux(self):
        serp = self.load_resource('search-for-linux')
        expected = ['126722-3927668', '12726-2848577', '4970-1206709']
        actual = extract_ranking_from_serp(serp)

        self.assertListEqual(expected, actual)

    def test_parsing_of_serp_for_linux_in_2014(self):
        serp = self.load_resource('search-for-linux-in-2014')
        expected = ['12726-2848577']
        actual = extract_ranking_from_serp(serp)

        self.assertListEqual(expected, actual)

    def test_parsing_of_serp_for_all_articles_at_2018_12_31(self):
        serp = self.load_resource('all-articles-at-2018-12-31')
        expected = [
                '70254-4154922', '110975-4154923', '70254-4154924',
                '65846-4154925', '117697-4154926', '65844-4154927',
                '116325-4154928', '110970-4154929', '110973-4154930',
                '52656-4154931', '110974-4154932', '115876-4154933',
                '108747-4154934', '117698-4154935', '108747-4154936',
                '43777-4154937', '75292-4154938', '4969-4154939',
                '110971-4154940', '110975-4154941', '110971-4154942',
                '11559-4154943'
        ]
        actual = extract_ranking_from_serp(serp)

        self.assertListEqual(expected, actual)

    def load_resource(self, resource):
        with open('test/resources/' + resource + '.html') as f:
            return f.read()
