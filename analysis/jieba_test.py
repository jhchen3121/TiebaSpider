#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

import nltk
import jieba
import sys
import json
import jieba.posseg as pseg
reload(sys)
sys.setdefaultencoding('utf8')

#path = u'/home/cjh/Desktop/TiebaSpider/data/嘤语词汇表.txt'

'''
source = open(path, 'r')
line = source.readline()
line = line.strip(' ')

while line!="":
    seglist = jieba.cut(line,cut_all=False)
    output = ' '.join(list(seglist)) 
    print output
'''
path = u'/home/cjh/Desktop/TiebaSpider/data/user_data/庆余年◆.txt'

with open(path, "r") as wf:
        txt = wf.read()
txt = txt.replace('\n', '')
txt = txt.strip()
txt = txt.split()
for text in txt:
    if text:
        #txt = jieba.cut(text)
        #print ", ".join(txt)
        words = pseg.cut(text)
        for word, flag in words:
            print ('%s %s' % (word, flag))
#fd = nltk.FreqDist(txt)
#keys=fd.keys()
#item=fd.iteritems()
#print ' '.join(keys)
#dicts=dict(item)
#sort_dict=sorted(dicts.iteritems(),key=lambda d:d[1],reverse=True)

#print json.dumps(sort_dict, ensure_ascii=False,encoding="gb2312")
