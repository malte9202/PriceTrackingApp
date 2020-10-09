from unittest import TestCase  # import unittest module
from Scraper import Scraper  # import Scraper class


class TestScraper(TestCase):
    def test_scrape_price(self):
        self.assertEqual(
            type(Scraper.scrape_price('https://geizhals.de/hisense-55a7100f-a2286242.html?hloc=at&hloc=de')),
            float, msg='price should be float')
        self.assertEqual(
            type(Scraper.scrape_price('https://geizhals.de/gigabyte-g27qc-a2304341.html?hloc=at&hloc=de')),
            float, msg='price should be float')
        self.assertEqual(
            type(Scraper.scrape_price('https://geizhals.de/apple-iphone-se-2020-64gb-schwarz-a2273374.html')),
            float, msg='price should be float')
        self.assertEqual(
            type(Scraper.scrape_price('https://geizhals.de/apple-macbook-air-space-gray-mwtj2d-a-a2255044.html')),
            float, msg='price should be float')
        self.assertEqual(
            type(Scraper.scrape_price('https://geizhals.de/apple-ipad-10-2-128gb-mw772fd-a-mw772ll-a-a2132800.html')),
            float, msg='price should be float')
