#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

import jieba
import jieba.analyse

def analyse_user_tag(filepath):
    '''
    分析出用户的关键字
    入口参数：
        filepath：文件路径
    返回值：
        user_name, tag
    '''

    user_name = filepath.split('/')[-1]
    user_name = user_name.split('.')[0]

    tag_list = []
    result_tag = ''

    text_from_file_with_path = open(filepath, 'r').read()
    for x, w in jieba.analyse.textrank(text_from_file_with_path, withWeight=True):
        #w为出现频率
        if w > 0.5:
            tag_list.append(x)

    str = ','
    result_tag = str.join(tag_list)

    return user_name, result_tag

if __name__ == '__main__':

    print analyse_user_tag('/home/cjh/Desktop/TiebaSpider/data/user_data/庆余年◆.txt')

