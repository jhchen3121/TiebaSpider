# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import
from lxml import etree
import sys
import requests
from selenium import webdriver
import time
import datetime
reload(sys)
sys.setdefaultencoding('utf8')

def buildurl():
    '''
    对贴吧热议的url进行构造
    :return: 返回一个热点标题的url列表
             以及对应的热议的title用于寻找存放的文件
    '''

    #url = 'https://tieba.baidu.com/mo/q/hotMessage/list'
    url = 'http://tieba.baidu.com/hottopic/browse/topicList?res_type=1'
    title_list = []
    topic_url_list = []
    #phantomjsdv = R"/home/cjh/Downloads/phantomjs-2.1.1-linux-x86_64/bin/phantomjs"
    #这里的requestsget方法访问url无法获得全部数据，因此此处使用selenium
    #这里的问题可以拿出来强调一下，为什么不用requests.get而用了selenium
    #drv = webdriver.PhantomJS(phantomjsdv)
    #drv.get(url)
    #html = etree.HTML(drv.page_source)
    #for line in html.xpath('//a[@class="block"]'):
    #    title = line.xpath('.//span[@class="word"]/text()')[0]
    #    title_list.append(title)
    #drv.quit()

    #for i in title_list:
        #print i
    #    pass

    #构造贴吧热议的url
    #for each_title in title_list:
    #    topic_url = 'http://tieba.baidu.com/hottopic/browse/hottopic?topic_name={}'.format(each_title)
    #    topic_url_list.append(topic_url)

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}

    reponse = requests.get(url, headers=headers).content

    html = etree.HTML(reponse)

    for each in html.xpath(r'//li[@class="topic-top-item"]'):
        topic_url = each.xpath(r'.//a[@class="topic-text"]/@href')[0]
        title = each.xpath(r'.//a[@class="topic-text"]/text()')[0]

        title_list.append(title)
        topic_url_list.append(topic_url)

        #print title
        #print topic_url
        
        #一个热议对应一个txt文件，里面存放所有帖子热议的内容，文件名就用对应的热议名
        #先创建每个日期所对应的文件夹，再根据文件夹创建每天的热议
        date = time.time()
        datetime_obj = datetime.datetime.fromtimestamp(date)
        daytime = datetime_obj.strftime("%Y-%m-%d")
        
        #创建目录
        path = r"/home/cjh/Desktop/TiebaSpider/data/hottopic_data/{}".format(daytime)
        mkdir(path)

        #创建文件
        open(r"/home/cjh/Desktop/TiebaSpider/data/hottopic_data/{time}/{title}.txt".format(time=daytime, title=title), "w").close()
        
    print "今天日期：{}".format(daytime)
    print "成功生成对应热议的txt文件!"
    
    #drv.quit()

    return topic_url_list, title_list


def mkdir(path):
    import os

    #路径处理
    path = path.strip()
    path = path.rstrip("\\")

    #判断路径是否存在
    isExists = os.path.exists(path)

    if not isExists:
        os.makedirs(path)
        
        return True
    else:
        return False
