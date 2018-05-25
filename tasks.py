#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

from workers import app_celery
from msgget import hot_mesg_get_by_celery
from msgget import user_mesg_get

import time
import random


#为celery加一个超时设置(超时为15min)
@app_celery.task(max_retries=3, soft_time_limit=900)
def celery_hottopic_spider(topic_url_list, title_list):
    '''
    异步爬虫
    '''
    hot_mesg_get_by_celery.tile_url_get(topic_url_list, title_list)

    #测试专用
    #print 'test'
    #time.sleep(random.randint(1,10))

    return 'END'

@app_celery.task
def celery_login_tieba(username, password):
    '''
    百度贴吧异步模拟登陆
    '''
    user_mesg_get.personal_tiezi_get(username, password)

    return 'END'
