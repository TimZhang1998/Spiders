from urllib.parse import urlencode
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import ErrorInResponseException
from config import *
from hashlib import md5
from multiprocessing import Pool
from json.decoder import JSONDecodeError
# import demjson
import requests
import json
import re
import pymongo
import os


client = pymongo.MongoClient(MONGO_URL, connect=False)
db = client[MONGO_DB]


def get_page_index(offset, keyword):
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': 1,
        'from': 'search_tab'
    }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('request index error', url)
        return None

def parse_page_index(html):
    # try:
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')
    # except JSONDecodeError:
        # pass

def get_page_detail(url):
    browser = webdriver.Chrome()
    try:
        browser.get(url)
        return browser.page_source
    except ErrorInResponseException:
        print('url response error')
    finally:
        browser.close()    
    '''
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36'}
    try:
        response = requests.get(url, headers = headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('request detail error', url)
        return None
    '''

def page_detail_parse(html, url):
    images = []
    soup = BeautifulSoup(html, 'lxml')
    title = soup.select('title')[0].get_text()
    print(title)
    '''
    images_pattern = re.compile(r'gallery: JSON.parse("(.*?)")', re.S)    # 无法匹配到json字符串  
    result = re.search(images_pattern, html)
    if result:
        data = json.loads(result.group(1))
        # data = demjson.decode(result.group(1))
        if data and 'sub_images' in data.keys():
            sub_images = data.get('sub_images')
            images = [item.get('url') for item in sub_images]
            return {
                'title': title,
                'url': url,
                'image': images
                }
    '''
    images_pattern = re.compile('<img src="(.*?)" data-src="(.*?)" alt="" />', re.S)
    results = re.findall(images_pattern, html)
    if results:
        for result in results:
            image = result[1]
            images.append(image)
            download_image(image)
        if images:
            return {
                'title': title,
                'url': url,
                'images': images
                }

def download_image(url):
    print('downloading ', url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            save_image(response.content)
        return None
    except RequestException:
        print('request image error', url)
        return None

def save_image(content):
    file_path = '{0}/images/{1}{2}'.format(os.getcwd(), md5(content).hexdigest(), '.jpg')
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()

def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('Successfully save to mongodb', result)
        return None
    return False


def main(offset):
    html = get_page_index(offset, KEYWORD)
    for url in parse_page_index(html):
        if url:
            html = get_page_detail(url)
            # print(html)
            if html:
                result = page_detail_parse(html, url)
                if result:
                    # print(result)
                    save_to_mongo(result)


if __name__ == '__main__':
    # main()
    groups =[x*20 for x in range(GROUP_START, GROUP_END + 1)] 
    pool = Pool()
    pool.map(main, groups)
    