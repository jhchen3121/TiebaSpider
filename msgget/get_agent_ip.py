#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import
import requests
from lxml import etree
import random

def get_ip_port():
    
    ip_list = []
    '''
    获取可用的代理高匿ip
    返回值:
        ip_list:IP地址:端口的列表
    '''
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
    }
    
    #获取前十页的高匿ip
    url_list = ['http://www.xicidaili.com/nn/{}'.format(i) for i in range(1,10)]
    for url in url_list:
        reponse = requests.get(url, headers=headers).content
        html = etree.HTML(reponse)
        for i in html.xpath('//tr[@class]'):
            x = i.xpath('.//td/text()')
            iptype = x[5]
            #删选类型为http的
            if iptype == 'HTTP':
                ip = x[0]
                port = x[1]
             
                each_ip = ip_build(ip, port)

                ip_list.append(each_ip)
    
    return ip_list

def ip_build(ip, port):
    '''
    代理ip构造，构造为HTTP://IP:PORT
    入口参数：
        ip：IP地址
        port：端口号
    返回值：
    ip_list:
        构造完成的ip
    '''
    finall_ip = 'http://{}:{}'.format(ip, port)
    finall_ip = {'http':finall_ip}
    
    return finall_ip

def choose_proxies():
    '''
    在可用的代理ip中选取一个
    返回值：
        proxies：可用的代理ip
    '''
    
    proxies = get_ip_port()
    proxies = random.choice(proxies)

    return proxies

