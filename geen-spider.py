# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

class PubSpider():
    # 固定的变量，包括地址，浏览器头部等
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    }
    PUBMED = 'https://www.ncbi.nlm.nih.gov/pubmed'
    GEENMED = 'http://geenmedical.com/search'

    def _post_response(self, url=GEENMED, query=None):
        r = requests.post(url, data=query, headers=self.HEADERS)
        return r.text

    # @classmethod
    def get_articles(self, query_string="egfr"):
        query_input = {"wb": query_string}
        response = self._post_response(query=query_input)
        soup = BeautifulSoup(response, "lxml")
        for i in soup.find_all('li'):
            print(i)
            print(i.find('div', class_='content-info').get_text())

        print('1')
        #print(response)




def run_spider():
    spider = PubSpider().get_articles('egfr')

if __name__ == '__main__':
    run_spider()
