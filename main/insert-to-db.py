# -*- coding: utf-8 -*-
import pymysql as ps
import googlecrawler

print(googlecrawler.TEST)


def insert_to_db(articles):
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
    cursor.lastrowid
    print('数据库连接成功')
    print(cursor.lastrowid)
    insert_to_article = """
    INSERT INTO nlp_article(`article_title`) 
    VALUES(%s)    
    """.format()
    # noinspection PyBroadException
    try:
        cursor.executemany(insert_to_article, articles)
        db.commit()
        print('数据导入成功')
    except:
        db.rollback()
        print('不知道哪儿出错')
    cursor.close()

