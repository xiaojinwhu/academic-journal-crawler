# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time

# ---------  一些固定变量   -----------#
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}
URL = 'https://scholar.google.com.hk/scholar'


# URL='www.baidu.com'


class GoCrawler:
    @staticmethod
    def _get_response(url=URL, query=None, verify=True, proxies=None):
        response = requests.get(url=url, params=query, headers=HEADERS, verify=verify, proxies=proxies)
        return response if response.status_code == 200 else print(response.status_code)

    """
    fetch_article方法可以传入从数据库传过来的迭代出来的list
    """

    def fetch_article(self, query_list):
        start = 0
        query_dict = {
            'q': query_list,
            'start': start,
            'btnG': '',
            'hl': 'zh-CN'
        }
        soup = BeautifulSoup(self._get_response(query=query_dict).text, "lxml")
        total_pages = soup.find_all('td')[-2].get_text()
        print(total_pages)
        limit = (int(total_pages) - 1) * 10
        # print(limit)
        articles = []  # 如果从外部传过来的lists进行迭代会有问题
        while limit >= start:
            for item in soup.find_all('div', class_='gs_r'):
                article_title = item.h3.get_text().replace('[HTML][HTML] ', '')
                ref_item = item.find('div', class_='gs_ggsd')
                article_ref = ref_item.a.get('href') if ref_item else 'null'
                citation = ''
                article_list = [
                    article_title,
                    article_ref,
                    query_list,
                    citation]
                articles.append(article_list)
            start += 10
        print(len(articles))

        return articles


#if __name__ == '__main__':
TEST = GoCrawler().fetch_article('"APC" AND "R653"')
