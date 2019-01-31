#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: TimZhang


"""
抓取百度贴吧---生活大爆炸吧的基本内容
爬虫线路： requests - bs4
Python版本： 3.6
OS： windows 10
"""


import requests

import time

from bs4 import BeautifulSoup


def get_html(url):
    """抓取页面源代码"""

    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        return "ERROR"


def get_content(url):
    """分析贴吧的网页文件，收集并整理信息，以字典的形式存储在列表里"""

    # 初始化一个列表存储所有的帖子信息
    contents = []
    # 抓取网页源代码
    html = get_html(url)
    # 用html源代码做一碗美味汤
    soup = BeautifulSoup(html, 'lxml')
    # 找到所有包含帖子信息的<li>标签(每个帖子信息都包含在一对<li>标签中)，并返回一个列表
    liTags = soup.find_all('li', attrs={'class': ' j_thread_list clearfix'})

    # 通过循环找到每个帖子中我们所需获取的信息
    for li in liTags:

        # 初始化一个字典储存每一个帖子的信息
        content = {}
        # 分别根据标签逐条获取帖子的信息
        try:
            content['title'] = li.find('a', attrs={'class': 'j_th_tit '}).text.strip()
            content['link'] = "http://tieba.baidu.com" + li.find('a', attrs={'class': 'j_th_tit '})['href']
            content['name'] = li.find('span', attrs={'class': 'tb_icon_author '}).text.strip()
            content['time'] = li.find('span', attrs={'class': 'threadlist_reply_date pull_right j_reply_data'}).text.strip()
            content['replyNum'] = li.find('span', attrs={'class': 'threadlist_rep_num center_text'}).text.strip()
            contents.append(content)
        except:
            print("Error in getting info")

    return contents


def out2file(dict):
    """将爬取到的信息输出到TBBT.txt文件"""

    with open('TBBT.txt', 'a+', encoding='utf-8') as f:
        for content in dict:
            f.write("标题：{} \t 链接：{} \t 发帖人：{} \t 最后回复时间：{} \t 回复数量：{} \n".format(\
                content['title'], content['link'], content['name'], content['time'], content['replyNum']))

    print("当前页面信息输出完成")


def main(base_url, deep):

    """初始化一个列表存储需要爬取的URL"""
    url_list = []
    for i in range(1, deep+1):
        url_list.append(base_url + '&pn=' + str(50 * (i-1)))
    print("所有网页已经全部下载到本地！准备开始爬取相关信息。。。")

    # 循环爬取每个页面上的信息并写入文件
    for url in url_list:
        contents = get_content(url)
        out2file(contents)
    print("所有的信息都已经保存完毕！")

# 设置基本的URL地址，不包括页面位置
base_url = 'http://tieba.baidu.com/f?kw=%E7%94%9F%E6%B4%BB%E5%A4%A7%E7%88%86%E7%82%B8&ie=utf-8'
# 设置需要爬取的页面数量
deep = 5

main(base_url, deep)

