import pandas as pd
import pymongo
from pymongo import MongoClient
import requests
from lxml import etree
import os

def get_html(url):
    """
    获取页面数据(文本)
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    }
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        return resp.text
    else:
        return None

def read_article_url():
    """
    读取MongoDB数据库中的文章链接（article_url）
    """
    client = MongoClient()
    db = client.JIANSHU
    collection = db.WEEKLY
    data = [i['article_url'] for i in collection.find()]
    return data

def parse_article_url_data(fileName, artiicle_url_data, db):
    """
    解释文章页面数据
    """
    root  = etree.HTML(artiicle_url_data)
    article_title = root.xpath('//div[@class="article"]/h1[@class="title"]/text()')[0] if root.xpath('//div[@class="article"]/h1[@class="title"]/text()') else ''
    article_content_selector = root.xpath('//div[@class="show-content"]')[0] if root.xpath('//div[@class="show-content"]') else ''
    article_content = article_content_selector.xpath('string()').strip() if article_content_selector else ""
    print(article_title + '\n', article_content)
    # save_data(db, artiicle_content)
    with open(fileName + '.txt',encoding="utf-8", mode='a') as f:
        f.write(article_title)
        f.write('\n')
        f.writelines(article_content)


def init_sql():
    """
    初始化数据库
    """
    client = MongoClient('localhost', 27017)
    db = client.JIANSHU
    return db


# def save_data(db, data):
#     """
#     保存数据到数据库中
#     """
#     db.ARTICLE.insert(data)


def main():
    article_urls = read_article_url()
    print(article_urls)

def test(db):
    article_urls = set(read_article_url())
    i = 0
    for article_url in article_urls:
        print(article_url)
        article_data = get_html(article_url)
        if article_data:
            parse_article_url_data(str(i), article_data, db)
        i += 1

if __name__ == '__main__':
    db = init_sql()
    test(db)
    