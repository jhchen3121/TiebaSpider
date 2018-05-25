# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import
from lxml import etree
import requests
import sys
import re
import time
import datetime
from selenium import webdriver
reload(sys)
sys.setdefaultencoding('utf8')

def tile_url_get(url, each_title):
    '''
    对相应热点进行内容的获取
    :param url_list: 一个url列表，存放不同热点消息的url
           title_list:对应热议标题的列表
    :return:
    '''

    #多变量循环zip
    #for url, each_title in zip(url_list, title_list):


        #FIXME这里改变抓取的方式，不在使用requests，利用selenium的phantomjs滚动条自动下来来获取更多的帖子的url
        #response = requests.get(url=url).content
        #html = etree.HTML(response)

        # driver = webdriver.PhantomJS(R"D:\phantomjs-2.1.1-windows\bin\phantomjs.exe")
        # driver.get(url)
        # html = etree.HTML(driver.page_source)
        # print driver.page_source

    phantdrv = R"/home/cjh/Downloads/phantomjs-2.1.1-linux-x86_64/bin/phantomjs"
    driver = webdriver.PhantomJS(phantdrv)
    driver.get(url)

    print "正在抓取热议：{}".format(each_title)
    
    #循环20次下拉至底部，尽可能的抓取全部url
    for i in range(1,20):
        #FIXME
        #下拉至底部的js部分代码，让phantomjs自动执行，长度尽可能的长10000000，也可以每次循环后自动叠加，待修改
        js="document.body.scrollTop=1000000"
        driver.execute_script(js)
        time.sleep(3)

    html = etree.HTML(driver.page_source)
    
    for line in html.xpath('//li[@class="thread-item"]'):
        #标题
        title = line.xpath('.//a[@class="title track-thread-title"]/text()')[0]
        #print title
        #每个帖子对应的url
        #这里帖子的url获取的不够全面，因为没有通过动态加载获取更多
        each_url = line.xpath('.//a[@class="title track-thread-title"]/@href')[0]
        each_url = 'http://tieba.baidu.com{}'.format(each_url)

        #url的重构，如果末尾带有?fid=*参数的需要去掉，因为要在结尾添加页面参数
        #FIXME
        #并不是每一个都是末尾fid带参数的，大多数都为空可以直接使用，因此不需要每次都执行正则，可以利用异常处理增加效率
        #正则表达式贪婪匹配
        #比较关键！！！
        each_url = re.sub(r'\?fid=(\d+)$',r'',each_url)

        print "对应帖子的标题：{}".format(title)

        each_note_mesg(each_url, each_title)

        #print each_url

    #每抓完一个热议，延时30s，防止过于频繁被封
    #time.sleep(30)

    print "已抓取完毕热议：{},存入对应的txt中".format(each_title)

def each_note_mesg(url, title):
    '''
    每个帖子的内容获取
    :param url: 对应帖子的url
           title:对应热议的标题
    :return:
    '''

    #两种不同方式的动态加载，不过速度还是差不多
    # crmdv = R"D:\chromedriver.exe"
    # drv = webdriver.Chrome(crmdv)
    # phantdv = R"D:\phantomjs-2.1.1-windows\bin\phantomjs.exe"
    # driver = webdriver.PhantomJS(phantdv)


    response = requests.get(url).content
    html = etree.HTML(response)

    #页数的获取
    #此处页面需要进行处理，有时候xpath获取到的页面值可能为空
    if len(html.xpath('//span[@class="red"]/text()')) >=2 :
        page = int(html.xpath('//span[@class="red"]/text()')[1])
    else:
        page = 1

    #从第一页开始获取各页的内容
    for index_page in range(1, page+1):
        #各个页面的url
        finall_url = url + "?pn={}".format(str(index_page))

        #使用request获取到页面数据之后，通过xpath来选取节点内容获取的是乱码
        #存在一些问题,编码问题已解决，解决方法如下,有些网页不是标准的unicode，因此需要用异常去处理
        response = requests.get(finall_url).content
        try:
            result = unicode(response, "utf-8")
        except BaseException:
            html = etree.HTML(response)
        else:
            html = etree.HTML(result)


        #drv与driver分别对应打开浏览器以及不打开，但是抓取数据的速度并没有差太多，因此最好还是要选择requests
        # drv.get(finall_url)
        # html = etree.HTML(drv.page_source)

        # driver.get(finall_url)
        # html = etree.HTML(driver.page_source)

        for sentence in html.xpath('//div[@class="d_post_content j_d_post_content  clearfix"]/text() | //div[@class="d_post_content j_d_post_content "]/text()'):
            #print sentence
            #通过对应的热议名称，把相关内容存入对应的txt文件中
            #需要对中文路径名称做处理
            date = time.time()
            datetime_obj = datetime.datetime.fromtimestamp(date)
            daytime = datetime_obj.strftime("%Y-%m-%d")

            filepath = u'/home/cjh/Desktop/TiebaSpider/data/hottopic_data/{daytime}/{title}.txt'.format(daytime=daytime, title=title)
            with open(filepath, "a+") as files:
                files.write(sentence + '\n')

