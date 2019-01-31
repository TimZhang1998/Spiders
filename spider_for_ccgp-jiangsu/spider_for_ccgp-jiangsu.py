#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: TimZhang


"""
抓取：无锡市环境监测中心站物业管理服务项目中标公告
爬虫线路：requests - bs4
Python版本：3.6
OS：windows 10
"""

import requests

import time

from bs4 import BeautifulSoup


def get_html(url):
	"""抓取页面源代码"""

	try:
		r = requests.get(url, timeout=30)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		return r.text
	except:
		return "ERROR"


def get_html_list(index_url, url_head):
	"""获取待爬取的网页列表"""
	
	html = get_html(index_url)
	soup = BeautifulSoup(html, 'lxml')
	
	div_tag = soup.find('div', attrs={'class': 'list_list'})
	
	a_tag_list = div_tag.find_all('a')
	
	url_list = []
	for a_tag in a_tag_list:
		url_list.append(url_head + a_tag['href'].strip('.'))
	
	return url_list
	
	
def get_index_url_list(url_head, deep):
	"""获取每页的url"""
	
	index_url_list = []
	index_url_list.append(url_head+'index.html')
	for i in range(1, deep):
		index_url_list.append(url_head+'index_'+str(i)+'.html')
	return index_url_list
	
	
def get_content(url):
	"""分析网页文件，收集并整理信息，以字典的形式存储在列表里"""

	content = {'url': ' ', 'title': ' ', 'text': ' '}
	content['url'] = url
	html = get_html(url)
	soup = BeautifulSoup(html, 'lxml')
	
	title_tag = soup.find('div', attrs={'class': 'dtit'})

	try:
		str_title = title_tag.find('h1').get_text()
		content['title'] = str_title.strip()
	except:
		print("Error in getting title")

	text_tag = soup.find('div', attrs={'class': 'detail_con'})

	try:
		detail_tag = text_tag.find_all('p')
		details = ''
		for detail in detail_tag:
			str_detail = detail.get_text()
			details = details + str_detail.strip()+ '\n'
		content['text'] = details
	except:
		print("Error in getting text")

	return content


def out2file(dict, i):
	"""将爬取到的内容输出到info.text"""
	
	file_name = "info"+str(i)
	
	with open('info/'+file_name+'.txt', 'a+', encoding='utf-8') as f:
		f.write('{}{}\n{}\n{}'.format("详情链接：", dict['url'], dict['title'], dict['text']))

	print("输出完毕！")


# 设置所要爬取的页数
deep = 15

# 设置所要爬取的栏目
url_head_list = ['http://www.ccgp-jiangsu.gov.cn/cgxx/cjgg/']

url_list_list = []

i = 1
for url_head in url_head_list:
	index_url_list = get_index_url_list(url_head, deep)
	for index_url in index_url_list:
		url_list_list.append(get_html_list(index_url, url_head))
	
for url_list in url_list_list:
	for url in url_list:
		try:
			content = get_content(url)
			out2file(content, i)
			i += 1
		except:
			print("跳过了一个顽皮的网页")
			continue

print('所有信息保存完毕！')
