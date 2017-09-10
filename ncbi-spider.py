# -*- coding: utf-8 -*-

import requests


class PubSpider():
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    }
    PUBMED = ''

    def _get_response(self, url):
        r = requests.get(url, params=None, headers=self.HEADERS)
        return r.text

    def get_articles(self, query):
        pass







def run_spider():
    spider = PubSpider()

if __name__ == '__main__':
    run_spider()
