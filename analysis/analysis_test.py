#!/usr/bin/env python
# -*- coding: utf-8 -*-

import jieba
import jieba.posseg as pseg
import codecs
import re
import os
import time
import string
from nltk.probability import FreqDist
open=codecs.open

def Chinese_Stopwords():          #导入停用词库
    stopword=[]
    cfp=open('empty.txt','r+','utf-8')   #停用词的txt文件
    for line in cfp:
        for word in line.split():
            stopword.append(word)
    cfp.close()
    return stopword

def Word_cut_list(word_str):
    #利用正则表达式去掉一些一些标点符号之类的符号。
    word_str = re.sub(r'\s+', ' ', word_str)  # trans 多空格 to空格
    word_str = re.sub(r'\n+', ' ', word_str)  # trans 换行 to空格
    word_str = re.sub(r'\t+', ' ', word_str)  # trans Tab to空格
    word_str = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——；！，”。《》，。：“？、~@#￥%……&*（）1234567①②③④)]+".\
                          decode("utf8"), "".decode("utf8"), word_str)

    wordlist = list(jieba.cut(word_str))#jieba.cut  把字符串切割成词并添加至一个列表
    wordlist_N = []
    chinese_stopwords=Chinese_Stopwords()
    for word in wordlist:
        if word not in chinese_stopwords:#词语的清洗：去停用词
            if word != '\r\n'  and word!=' ' and word != '\u3000'.decode('unicode_escape') \
                    and word!='\xa0'.decode('unicode_escape'):#词语的清洗：去全角空格
                wordlist_N.append(word)
    return wordlist_N

def Word_pseg(word_str):  # 名词提取函数
    words = pseg.cut(word_str)
    word_list = []
    for wds in words:
        # 筛选自定义词典中的词，和各类名词，自定义词库的词在没设置词性的情况下默认为x词性，即词的flag词性为x
        if wds.flag == 'x' and wds.word != ' ' and wds.word != 'ns' \
                or re.match(r'^n', wds.flag) != None \
                        and re.match(r'^nr', wds.flag) == None:
            word_list.append(wds.word)
    return word_list

def sort_item(item):#排序函数，正序排序
    vocab=[]
    for k,v in item:
        vocab.append((k,v))
    List=list(sorted(vocab,key=lambda v:v[1],reverse=1))
    return List

def Run():
    Apage=open(u'/home/cjh/Desktop/TiebaSpider/data/hottopic_data/2018-01-26/解忧杂货店.txt','r+','utf-8')
    Word=Apage.read()                       #先读取整篇文章
    Wordp=Word_pseg(Word)              #对整篇文章进行词性的挑选
    New_str=''.join(Wordp)
    Wordlist=Word_cut_list(New_str)    #对挑选后的文章进行分词
    Apage.close()
    return  Wordlist

if __name__=='__main__':

    wl = Run()
    fdist = FreqDist(wl)
    Sum = len(wl)
    pre = 0
    for (s, n) in sort_item(fdist.items()):
        print s + str(float(n) / Sum)+"      " +str(n)+ '\r\n'
        pre = pre + float(n) / Sum
        #if pre > 0.5:
        #    print str(pre)
        #    break


