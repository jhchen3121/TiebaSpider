#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import
from lxml import etree
import sys
import re
import json
import time
from login import login_selenium
import requests
from msgget import get_agent_ip
from selenium import webdriver

reload(sys)
sys.setdefaultencoding('utf8')

def user_name_get(username, passwd):
    
    '''
    用户的用户名获取
    '''

    cookie = login_selenium.login_cookieget(username, passwd)
    
    #url = 'https://tieba.baidu.com'
    #url = 'http://tieba.baidu.com/i/i/my_tie'
    url = 'https://passport.baidu.com/center'
    headers = {
        'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Mobile Safari/537.36',
    }
    cookies = {
        'Cookie' : cookie,    
    }

    reponse = requests.get(url, cookies=cookies, headers=headers).content

    html = etree.HTML(reponse)
    name = html.xpath('//div[@class="mod-personal-name"]/text()')[0]
    print name
    #print reponse
    #with open("a.html",'wb') as f:
    #    f.write(reponse)
    #    f.close()

def tieba_concern_get(username, passwd):

    '''
    用户所关注的贴吧获取
    '''
    #选取一个高匿ip做代理ip
    proxies = get_agent_ip.choose_proxies()

    cookie = login_selenium.login_cookieget(username, passwd)
    url = 'https://tieba.baidu.com'
    headers = {
        'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Mobile Safari/537.36',
    }

    cookies = {'Cookie' : cookie}

    reponse = requests.get(url, cookies=cookies, headers=headers, proxies=proxies).content
    html = etree.HTML(reponse)

    for i in html.xpath('//div[@class="forumTile_name"]/text()'):
        print i
    #贴吧等级看情况考虑
    #for i in html.xpath('//div[@class="level"]/text()'):
    #    print i
    #print reponse

    #尝试抓取用户所发过帖子的内容,requests方法抓取存在一些问题，尝试使用selenium来抓取
    #reponse = requests.get(url='http://tieba.baidu.com/i/i/my_tie?&pn=1', cookies=cookies, headers=headers).content
    #print reponse


def personal_tiezi_get(username, passwd):
    '''
    用户所发帖子获取
    '''

    #创建用户发帖内容文件
    
    #此处通过模拟登陆获取driver
    driver = login_selenium.login_cookieget(username, passwd)

    url = 'http://tieba.baidu.com/i/i/my_tie?&pn=1'

    #获取用户名
    driver.get(url)
    time.sleep(2)
    html = etree.HTML(driver.page_source)
    try:
        user_name = html.xpath(r'//p[@class="aside_user_name"]/text()')[0]

        #创建用户发帖内容文件
        filepath = r"/home/cjh/Desktop/TiebaSpider/data/user_data/{}.txt".format(user_name)
        open(filepath, "w").close()

        print '用户{}文件创建成功！'.format(user_name)
    except BaseException:
        print '获取用户名失败!'

    #用户可能发了比较多的帖子，也可能比较少，暂时只取前10页
    #构造前十页的url
    #FIXME
    for i in range(1,11):
        url = 'http://tieba.baidu.com/i/i/my_tie?&pn={}'.format(i)
        driver.get(url)
        time.sleep(2)
        html = etree.HTML(driver.page_source)

        #获取所发帖子的url
        for each in html.xpath(r'//li'):

            #进行异常判断，如果不存在则为空
            try:
                user_url = each.xpath(r'.//a[@class="thread_title"]/@href')[0]
                title = each.xpath(r'.//a[@class="thread_title"]/text()')[0]
            except BaseException:
                user_url = None
                title = None

            
            #每个url缺少前缀，还需要重新构造
            #注：初始url格式为https://tieba.baidu.com/p/3726446415?pid=67574329523&cid=0#67574329523
            #注：需要构造成只看楼主的urlhttps://tieba.baidu.com/p/3943869119?see_lz=1，即利用正则表达式去掉后部分
            if user_url:
                user_url = re.sub(r'\?pid=(\d+)', '', user_url)
                user_url = re.sub(r'\&cid=0#(\d+)', '', user_url)
                user_url = user_url + '?see_lz=1'
                user_url = 'https://tieba.baidu.com{}'.format(user_url)
                
                #开始获取内容
                get_only_user_msg(user_url, filepath, title)

        return filepath

    #清除所有的cookie
    #driver.delete_all_cookies()
    #driver.get(url)

    #访问带上cookie
    #driver.add_cookie(cookie)
    #time.sleep(2)
    #driver.refresh()

    #print driver.page_source
    #html = etree.HTML(driver.page_source)
    
def get_only_user_msg(url, filepath, title):
    '''
    只获取用户所发表的楼层言论，并写入至对应的文件夹
    '''

    #先获取各个帖子的页数
    #proxies = get_agent_ip.choose_proxies()
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}

    reponse = requests.get(url, headers=headers).content

    html = etree.HTML(reponse)
    
    try:
        page = html.xpath(r'//span[@class="red"]/text()')[1]
    except BaseException:
        print '页数获取错误'

    print '正在获取帖子：{}的内容'.format(title)

    #根据对应的页数重新构造url并获取每页的内容
    for index in range(1, int(page)+1):
        #重构url重新访问
        #此时的url格式为https://tieba.baidu.com/p/5267731347?see_lz=1
        url = re.sub(r'\?see_lz=(\d+)', '', url)
        url = url + '?see_lz={}'.format(str(index))
        
        reponse = requests.get(url, headers=headers).content
        #乱码异常处理
        try:
            result = unicode(reponse, "utf-8")
        except BaseException:
            html = etree.HTML(reponse)
        else:
            html = etree.HTML(result)

        #贴吧楼层有不同的样式，一个for循环存放一个样式的div class
        #for line in html.xpath(r'//div[@class="d_post_content_main "]'):
            #这里需要注意
            #FIXME
            #不同用户可能用了一些贴吧的特效标签，因此divclass也是有区别的，这里暂时先填自己的样式
            #图片的异常判断，图片是取不到的
            #还有几个帖子的内容无法获取到
        #    try:
         #       sentence = line.xpath(r'.//div[@class="post_bubble_middle_inner"]/text()')[0]
          #      print sentence
          #  except BaseException:
                #用户此时发的可能是图片表情，因此获取不到内容，跳过
           #     continue

            #with open(filepath, "a+") as files:
             #   files.write(sentence + '\n')

        #此处存放第二个样式class
        #for line in html.xpath(r'//div[@class="d_post_content_main  d_post_content_firstfloor"]'):
            #这里需要注意
            #FIXME
            #不同用户可能用了一些贴吧的特效标签，因此divclass也是有区别的，这里暂时先填自己的样式
            #图片的异常判断，图片是取不到的
            #还有几个帖子的内容无法获取到
         #   try:
          #      sentence = line.xpath(r'.//div[@class="d_post_content j_d_post_content "]/text()')[0]
           #     print sentence
           # except BaseException:
                #用户此时发的可能是图片表情，因此获取不到内容，跳过
          #      continue

           # with open(filepath, "a+") as files:
            #    files.write(sentence + '\n')
        
        xpath_first = r'//div[@class="d_post_content_main "]'
        xpath_second = r'.//div[@class="post_bubble_middle_inner"]/text()'
        xpath_third = r'//div[@class="d_post_content_main  d_post_content_firstfloor"]'
        xpath_forth = r'.//div[@class="d_post_content j_d_post_content "]/text()'
        find_all_msg(xpath_first, xpath_second, html, filepath)
        find_all_msg(xpath_third, xpath_forth, html, filepath)
        find_all_msg(xpath_first, xpath_forth, html, filepath)
        find_all_msg(xpath_third, xpath_second, html, filepath)


def find_all_msg(xpath_first, xpath_second, html, filepath):
    '''
    由于贴吧的帖子楼层的div有不同的排列组合方式，因此通过传参来统一调用函数
    '''
    for line in html.xpath(xpath_first):
        try:
            sentence = line.xpath(xpath_second)[0]
            print sentence
        except BaseException:
            continue
        with open(filepath, "a+") as files:
            files.write(sentence + '\n')
