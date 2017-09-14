# -*- coding: utf-8 -*-

import requests
import pymysql as ps
from scrapy.selector import Selector

db_config = {
    'host': '10.10.172.41',
    'port': 3306,
    'user': 'xj',
    'password': 'xj3d',
    'db': 'dspdw_dev',
    'charset': 'utf8'
}
db = ps.connect(**db_config)
cursor = db.cursor()
print('数据库连接成功')


def ip_spider():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }
    for i in range(2093):
        re = requests.get("http://www.xicidaili.com/nn/{0}".format(i), headers=headers)
        selector = Selector(text=re.text)
        all_trs = selector.css("#ip_list tr")
        ip_list = []
        for tr in all_trs[1:]:
            speed_str = tr.css(".bar::attr(title)").extract()[0]
            if speed_str:
                speed = float(speed_str.split("秒")[0])
            ip = tr.css("td:nth-child(2)::text").extract_first()
            port = tr.css("td:nth-child(3)::text").extract_first()
            proxy_type = tr.css("td:nth-child(6)::text").extract_first()
            ip_list.append((ip, port, proxy_type, speed))
        for ip_info in ip_list:
            cursor.execute(
                "insert proxy_ip(ip, port, speed, proxy_type) VALUES('{0}', '{1}', '{2}', '{3}')".format(
                    ip_info[0], ip_info[1], ip_info[3], ip_info[2]
                )
            )
            db.commit()

class GetIP:
    def delete_ip(self, ip):
        """
        从数据库中删除无效的IP 
        """
        delete_sql = "DELETE FROM proxy_ip WHERE ip='{0}'".format(ip)
        cursor.execute(delete_sql)
        db.commit()
        return True

    def judge_ip(self, ip, port):
        """
        判断IP是否可用
        """
        http_url = "http://www.baidu.com"
        proxy_url = "http://{0}:{1}".format(ip, port)
        try:
            proxy_dict = {
                "http": proxy_url,
            }
            response = requests.get(http_url, proxies=proxy_dict)
        except Exception as e:
            print("invalid ip and port")
            self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            if 200 <= code < 300:
                print("effective ip")
                return True
            else:
                print("invalid ip and port")
                self.delete_ip(ip)
                return False

    def get_random_ip(self):
        """
        从数据库中随机获取一个可用的IP
        """
        random_sql = """
                SELECT ip, port FROM proxy_ip
                ORDER BY RAND()
                LIMIT 1
            """
        result = cursor.execute(random_sql)
        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]
            judge_re = self.judge_ip(ip, port)
            if judge_re:
                return "http://{0}:{1}".format(ip, port)
            else:
                return self.get_random_ip()

if __name__ == '__main__':
    #ip_spider()
    get_ip = GetIP()
    get_ip.get_random_ip()
