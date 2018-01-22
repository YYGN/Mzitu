# !/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo
import requests
from setting import *
from requests.exceptions import ProxyError
from lxml import etree
from hashlib import md5
import os
import redis
import random
from urllib3.exceptions import NewConnertionError, MaxRetryError


def get_html(url=None, headers=None, proxy=None):
    url = url if url else START_URL
    headers = headers if headers else DEFAULT_USER_AGENT
    proxy = proxy
    if proxy:
        if isinstance(proxy, bytes)
        proxy = proxy.decode('utf-8')
        print('正在使用代理IP %s' % proxy)
        try:
            response = requests.get(url, headers=headers, proxies=proxy)
            if response.status_code == 200:
                response.encoding = response.apparent_encoding
                return response.text
        except (ConnectionRefusedError, NewConnectionError, MaxRetryError, ProxyError) as e:
            print('Error happend goes %s' % e)
            
def get_proxy():
    if PASSWORD:
        redisClient = redis.Redis(host=HOST, port=PORT, password=PASSWORD)
    else:
        redisClient = redis.Redis(host=HOST, port=PORT)
    proxies = redisclient.lrange('proxies', 0, -1)
    return random.choice(proxies)


def parse_html(html):
    print('正在获取全部图集......')
    doc = etree.HTML(html)
    titles = doc.xpath('//p/a/text()')
    gallery = doc.xpath('//ul[@class="archives"]/li/p[2]/a/@href')
    print('总共有{}个结果'.format(len(titles)))
    for title, link in zip(titles, gallery):
        result =  {
        'title': title,
        'url': link
        }
        save_to_mongo(result)
    return gallery


def parse_detail(url):
    proxy = get_proxy()
    print('正在解析页面%s' % url)
    html =get_html(url=url, proxy=proxy)
    if type(html) == str:
        doc = etree.HTML(html)
        max_pages = doc.xpath('//div[@class="pagenavi"]/a[5]/span/text()')
        if max_pages:
            int_pages = int(max_pages[0])
            image_url_list = [url + '/' + str(page) for page in range(1, max_pages+1)]
            for image_url in image_url_list:
                html = get_html(url=image_url)
                get_image_link(html)
            


def get_image_link(html):
    doc = etree.HTML(html)
    title = doc.xpath('//div[@class="main-image"]/p/a/img/@alt')[0]
    image_link = doc.xpath('//div[@class="main-image"]/p/a/img/@src')[0]
    get_content(image_link, title)


def get_content(image_link, title):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh_CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Referer': image_link
    }
    try:
        response = requests.get(image_link, headers=headers)
        content = response.content
        save_image(content, title)
    except exceptions:
        print('Something just wrong.')


def save_image(content, title):
    store_path = IMAGES_STORE + title
    if not os.path.exists(store_path):
        os.mkdir(store_path)
    file_name = md5(content).hexdigest() + '.jpg'
    file_path = store_path + '/' +file_name
    if not os.path.exists(file_path):
        print('正在保存图片%s' % file_name)
        with open(file_path, 'wb')as f:
            f.write(content)
            f.close()
    else:
        print('图片已存在%s' % file_name)


def save_to_mongo(images):
    client = pymongo.MongoClient(host=MONGO_URL)
    db = client[MONGO_DATABASE]
    try:
        if db[MONGO_TABLE].insert(images):
            print('保存到MongoDB成功')
    except:
        print('存储到MongoDB失败')
