import requests
from lxml import etree

homepage_url = 'http://www.jianshu.com'
base_url = 'http://www.jianshu.com/trending/weekly'


def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    }
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        return resp.text
    else:
        return None


def parse_first_html(html, db):
    """
    解析首页数据
    """
    root = etree.HTML(html)
    articles = root.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "content", " " ))]')
    seen_snote_ids = root.xpath('//ul[@class="note-list"]/li/@data-note-id')
    # print(seen_snote_ids)
    for article in articles:
        author = ''.join(article.xpath('div[@class="author"]/div[@class="name"]/a/text()'))
        author_url = homepage_url + ''.join(article.xpath('div[@class="author"]/div[@class="name"]/a/@href'))
        title = ''.join(article.xpath('a[@class="title"]/text()'))
        article_url = homepage_url + ''.join(article.xpath('a[@class="title"]/@href'))
        abstract = ''.join(article.xpath('p[@class="abstract"]/text()')).strip()
        tag = ''.join(article.xpath('div/a[class="collection-tag"]/text()'))
        read_and_comments = article.xpath('div[@class="meta"]/a/text()')
        like_and_pay = article.xpath('div[@class="meta"]/span/text()')
        # 数据处理
        read_and_comments = ''.join(read_and_comments).strip().split()
        like_and_pay = ''.join(like_and_pay).strip().split()
        # read_count = meta.xpath('a/text()')
        # print(author, author_url, title, article_url, abstract, read_and_comments, like_and_pay)
        # print(''.join(like_and_pay).strip().split())
        data ={
            'author': author,
            'author_url': author_url,
            'title': title,
            'article_url': article_url,
            'abstract': abstract,
            'read_and_comments': read_and_comments,
            'like_and_pay': like_and_pay
        }
        if not is_data_exist(db, data):
            print('保存新数据')
            save_data(db, data)
        else:
            print('数据已存在，更新数据')
            update_data(db, data)
    return seen_snote_ids


def parse_other_html(html, db):
    root = etree.HTML(html)
    articles = root.xpath('//li/div[@class="content"]')
    seen_snote_ids = root.xpath('//li/@data-note-id')
    # print(seen_snote_ids)
    for article in articles:
        author = ''.join(article.xpath('div[@class="author"]/div[@class="name"]/a/text()'))
        author_url = homepage_url + ''.join(article.xpath('div[@class="author"]/div[@class="name"]/a/@href'))
        title = ''.join(article.xpath('a[@class="title"]/text()'))
        article_url = homepage_url + ''.join(article.xpath('a[@class="title"]/@href'))
        abstract = ''.join(article.xpath('p[@class="abstract"]/text()')).strip()
        read_and_comments = article.xpath('div[@class="meta"]/a/text()')
        like_and_pay = article.xpath('div[@class="meta"]/span/text()')
        # 数据处理
        read_and_comments = ''.join(read_and_comments).strip().split()
        like_and_pay = ''.join(like_and_pay).strip().split()
        data ={
            'author': author,
            'author_url': author_url,
            'title': title,
            'article_url': article_url,
            'abstract': abstract,
            'read_and_comments': read_and_comments,
            'like_and_pay': like_and_pay
        }
        if not is_data_exist(db, data):
            print('保存新数据')
            save_data(db, data)
        else:
            print('数据已存在，更新数据')
            update_data(db, data)
    return seen_snote_ids


def get_other_html(url, page, seen_snote_ids):
    url_param = url
    page_param = str(page)
    seen_snote_ids_param = '?seens_snote_ids%5B%5D=' + '?seens_snote_ids%5B%5D='.join(seen_snote_ids)
    url = url + '?page=' + page_param + seen_snote_ids_param
    # print(url)
    return get_html(url)


def init_sql():
    """
    初始化数据库
    """
    from pymongo import MongoClient
    client = MongoClient('localhost', 27017)
    # 创建数据库sdifen
    db = client.JIANSHU
    return db


def save_data(db, data):
    """
    保存数据到数据库中
    """
    db.WEEKLY.insert(data)


def update_data(db, data):
    """
    更新数据：删除原数据，重新保存该数据？？？
    """
    pass

def is_data_exist(db, data):
    """
    判断数据库中是否存在数据
    """
    return db.WEEKLY.find({'article_url': data.get('article_url')}).count()

def main():
    db = init_sql()
    resp = get_html(base_url)
    seen_snote_ids = parse_first_html(resp, db) 
    for i in range(2, 15):
        resp = get_other_html(base_url, i, seen_snote_ids)
        seen_snote_ids.extend(parse_other_html(resp, db))


if __name__ == '__main__':
    main()
