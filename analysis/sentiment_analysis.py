#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import
import os
import codecs
import re
import numpy as np
import pymysql
import time
from snownlp import SnowNLP
import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt
from snownlp import sentiment
from snownlp.sentiment import Sentiment

#comment = []
#with open(u'/home/cjh/Desktop/TiebaSpider/data/hottopic_data/2018-01-26/解忧杂货店.txt', mode='r', encoding='utf-8') as f:
#    rows = f.readlines()
#    for row in rows:
#        if row not in comment:
#            comment.append(row.strip('\n'))

def build_comment():
    '''
    循环遍历今日的所有热议内容，存放至list中
    '''
    comment = []

    base_path = u'/home/cjh/Desktop/TiebaSpider/data/hottopic_data/'
    datetime = time.strftime("%Y-%m-%d", time.localtime())

    #遍历出所有的文件txt
    file_path = base_path + datetime
    #测试数据
    #file_path = u'/home/cjh/Desktop/TiebaSpider/data/hottopic_data/2018-04-23'
    for i in os.walk(file_path):
        file_name_list = i

    file_name_list = file_name_list[2]

    for eachfile in file_name_list:
        eachfile_path = file_path + '/' + eachfile

        with open(eachfile_path, mode='r', encoding='utf-8') as f:
            rows = f.readlines()
            for row in rows:
                if row not in comment:
                    comment.append(row.strip('\n'))

    return comment

def snowanalysis(self):
    '''
    利用snownlp分析，把分析结果存入对应的日期的分析结果中
    '''
    sentimentslist = []
    #句子以行为单位存入list中， 因此每次分析都是以行为单位
    for li in self:
        #print(li)
        try:
            #实例化
            s = SnowNLP(li)
        except:
            continue
        print(s.sentiments)
        sentimentslist.append(s.sentiments)

    plt.hist(sentimentslist, bins=np.arange(0, 1, 0.01))
    plt.show()

    path = u'/home/cjh/Desktop/TiebaSpider/data/analysis_data/'
    datetime = time.strftime("%Y-%m-%d", time.localtime())

    path = path + datetime
    plt.savefig(path + '/' + 'sentiments.jpg')

if __name__ == '__main__':


    start_time = time.time()

    comment = build_comment()

    snowanalysis(comment)

    end_time = time.time()

    print (end_time - start_time)
