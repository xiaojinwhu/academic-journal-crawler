# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

class PubSpider():
    # 固定的变量，包括地址，浏览器头部等
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    }
    PUBMED = 'https://www.ncbi.nlm.nih.gov/pubmed'
    GEENMED = 'http://geenmedical.com/search'

    def _get_response(self, url=GEENMED, query=None):
        r = requests.get(url, params=query, headers=self.HEADERS)
        return r.text

    # @classmethod
    def get_articles(self, query_string="egfr"):
        query_input = {"wb": query_string}
        response = self._get_response(query=query_input)
        soup = BeautifulSoup(response, "lxml")
        print(soup)

        # articles = []
        # ----------  下面是 爬取pubmed的代码   --------
        # response = self._get_response(url=self.PUBMED, query=query)
        # soup = BeautifulSoup(response, "lxml")
        # for article in soup.find_all('div', class_='rprt'):
        #     article_title = article.p.get_text().replace('<i>', '').replace('</i>', '')
        #     # print(article_title)
        #     article_pmid = article.find('dd').get_text()
        #     article_detail_url = 'https://www.ncbi.nlm.nih.gov/pubmed' + '/' + article_pmid
        #     print(article_detail_url)
        #     r = self._get_response(article_detail_url)
        # print(r)






def run_spider():
    spider = PubSpider().get_articles()

if __name__ == '__main__':
    run_spider()
