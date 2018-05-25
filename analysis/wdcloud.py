#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import
import pickle
import os
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image
import numpy as np
import time
import datetime
import random
from util import db

def make_wordcloud(date, filepath):
    '''
    生成词云图片,无返回值，对应图片存储到对应的文件夹中，以日期格式命名
    入口参数：
        date:日期参数，用于存放对应的文件路径
        file_path:对应文本的路径，用于解析生成词云
    '''

    #出去末尾的.txt
    filepath = filepath[:-4]
    file_path = "/home/cjh/Desktop/TiebaSpider/data/hottopic_data/{time}/{title}.txt".format(time=date, title=filepath)

    text_from_file_with_path = open(file_path, 'r', encoding='UTF-8').read()
    wordlist_after_jieba = jieba.cut(text_from_file_with_path, cut_all=False)
    wl_space_split = " ".join(wordlist_after_jieba)

    print (wl_space_split)

    #background_Image = plt.imread(r'./222.png')
    #这里的背景图片加载使用了numpy，ply加载图片会有问题
    #此处添加一些多样性的图片，然后构成一个图片库，随机选取
    d = os.path.dirname(__file__)
    num = random.randint(1,10)
    bkgd_image = '{}.png'.format(num)
    background_Image = np.array(Image.open(os.path.join(d, bkgd_image)))
    
    print ('加载图片成功')

    '''设置样式'''
    stopwords = STOPWORDS.copy()
    stopwords.add('哈哈')
    stopwords.add('啊')#屏蔽词设置

    wc = WordCloud(
        #width=328,#宽度
        #height=328,#高度
        background_color='white',#图片背景色
        mask=background_Image,#背景图片样式
        font_path=r'/home/cjh/Desktop/TiebaSpider/simsun.ttf',#中文字体
        max_words=300,#最大字数
        stopwords=stopwords,#设置停用词
        max_font_size=400,#字体大小最大值
        random_state=50,#配色方案种类
    )

    wc.generate_from_text(wl_space_split)#开始加载文本
    img_colors = ImageColorGenerator(background_Image)
    wc.recolor(color_func=img_colors)#字体颜色为背景图片颜色
    plt.imshow(wc)#显示词云图
    plt.axis('off')#是否显示x，y轴坐标
    plt.show()
    #plt.savefig('wdtest.png')


    #获得模块所在的路径
    #d = path.dirname(__file__)
    path = '/home/cjh/Desktop/TiebaSpider/data/analysis_data/{time}'.format(time=date)
    wc.to_file(os.path.join(path, "{}.jpg".format(filepath)))
    print ('生成词云成功')

    #此处把图片，时间，title存放至对应数据库的表中
    title = filepath
    img_path = '/home/cjh/Desktop/TiebaSpider/data/analysis_data/{time}/{path}.jpg'.format(time=date, path=filepath)
    db.hottopic_inster(date, title, img_path)

def get_today_all_txt():
    '''
        获取今日所有内容的txt
        入口参数：
            无
        返回值：
            无
    '''

    filename_list = []

    date = time.time()
    datetime_obj = datetime.datetime.fromtimestamp(date)
    daytime = datetime_obj.strftime("%Y-%m-%d")


    ###############################
    #     用于测试的日期          #
    ###############################
    #daytime = '2018-03-08'
    
    #重新拼接一下路径，使用绝对路径的方式
    #for i in filename_all:
    #    path = u'/home/cjh/Desktop/TiebaSpider/data/hottopic_data/{daytime}/{filename}'.format(daytime=daytime, filename=i)
    #    filename_list.append(path)
    
    #print (filename_list)
    #return filename_list
    
    #创建目录
    path = r"/home/cjh/Desktop/TiebaSpider/data/analysis_data/{}".format(daytime)
    mkdir(path)

    #根据日期去查找对应的文件夹
    path = u'/home/cjh/Desktop/TiebaSpider/data/hottopic_data/{daytime}'.format(daytime=daytime)
    #文件夹内容的遍历
    print (path) 
    for each_filename in os.walk(path):
        print (each_filename)
        #由于循环出来的最后一个默认为list，因此直接等就好
        filename_all = each_filename[2]

    #依次分析日常的txt内容
    for each_filename in filename_all:
        #判断txt中是否有内容
        file_path = "/home/cjh/Desktop/TiebaSpider/data/hottopic_data/{time}/{title}".format(time=daytime, title=each_filename)
        text_from_file_with_path = open(file_path, 'r', encoding='UTF-8').read()
        if text_from_file_with_path == '':
            continue

        make_wordcloud(daytime, each_filename)
    
def mkdir(path):
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

#if __name__ == '__main__':
    
#    get_today_all_txt()
