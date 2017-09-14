# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time
from ipspider import GetIP

"""
谷歌学术爬虫类GooSpider()
提供的方法：

"""

# ---------  一些固定变量   -----------#
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}
URL = 'https://scholar.google.com.hk/scholar'
ROOT = 'D://'

class GoSpider:
    def __init__(self):
        pass

    @staticmethod
    def _get_response(url=URL, query=None, verify=True, proxies=None):
        response = requests.get(url=url, params=query, headers=HEADERS, verify=verify, proxies=proxies, timeout=10)
        return response if response.status_code == 200 else print('不能连接到服务器')

    """
    fetch_article方法可以传入从数据库传过来的迭代出来的list
    """

    def fetch_article(self, query_list, limit=20, download=False):
        start = 10
        query_dict = {
            'q': query_list,
            'start': start
        }
        soup = BeautifulSoup(self._get_response(query=query_dict).text, "lxml")
        # total_pages = len(soup.find_all('td')) - 2
        articles = []  # 如果从外部传过来的lists进行迭代会有问题
        while limit >= start:
            for item in soup.find_all('div', class_='gs_r'):
                article_title = item.h3.get_text().replace('[HTML][HTML] ', '')
                ref_item = item.find('div', class_='gs_ggsd')
                article_ref = ref_item.a.get('href') if ref_item else 'null'
                citation = ''
                article_list = [article_title, article_ref, query_list, citation]
                articles.append(article_list)
                print(article_title)
            start += 10
        return articles

    #     if download:
    #         for i, li in enumerate(articles):
    #             if li[1].endswith('.pdf'):
    #                 # noinspection PyBroadException
    #                 try:
    #                     find_pdf = self._get_response(li[1]).content
    #                     time.sleep(3)
    #                     pdf_name = li[1].split('/')[-1]
    #                     self._save_pdf(pdf_name,find_pdf)
    #                 except:
    #                     print('有点问题,采取sci-hub试试')
    #             else:
    #                 print('尝试通过sci-hub下载，希望不要出现验证码')
    #                 url_to_sci = 'http://sci-hub.cc/' + li[0]
    #                 while True:
    #                     ip = GetIP().get_random_ip()
    #                     random_proxy = {
    #                         'http': ip,
    #                         'https': ip
    #                     }
    #                     r = self._get_response(url_to_sci, verify=False, proxies=random_proxy)  # verify = False
    #                     if r.headers['Content-Type'] != 'application/pdf':
    #                         print(ip)
    #                         continue
    #                     else:
    #                         self._save_pdf(li[0], r.content)
    #             print('文献下载完成')
    #
    # def _save_pdf(self, pdf_name, content):
    #     path = ROOT + pdf_name
    #     time.sleep(3)
    #     with open(path, 'wb') as f:
    #         f.write(content)
    #         print('PDF保存成功')
    #         f.close()
def save_pdf(pdf_name, content):
    path = ROOT + pdf_name
    time.sleep(3)
    with open(path, 'wb') as f:
        f.write(content)
        print('PDF保存成功')
        f.close()

def download(articles):
    for i, li in enumerate(articles):
        if li[1].endswith('.pdf'):
            # noinspection PyBroadException
            try:
                find_pdf = self._get_response(li[1]).content
                time.sleep(3)
                pdf_name = li[1].split('/')[-1]
                self._save_pdf(pdf_name,find_pdf)
            except:
                print('有点问题,采取sci-hub试试')
        else:
            print('尝试通过sci-hub下载，希望不要出现验证码')
            url_to_sci = 'http://sci-hub.cc/' + li[0]
            while True:
                ip = GetIP().get_random_ip()
                random_proxy = {
                    'http': ip,
                    'https': ip
                }
                r = self._get_response(url_to_sci, verify=False, proxies=random_proxy)  # verify = False
                if r.headers['Content-Type'] != 'application/pdf':
                    print(ip)
                    continue
                else:
                    self._save_pdf(li[0], r.content)
        print('文献下载完成')



if __name__ == '__main__':
    goo = GoSpider().fetch_article('egfr', download=False)
    #download(goo)
