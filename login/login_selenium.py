#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

import time
import json
import re
import requests
import rsa
import base64
import sys
from selenium import webdriver
reload(sys)
sys.setdefaultencoding('utf8')


def login_cookieget(name, passwd):
    '''
    模拟登陆百度，获取登陆时的cookie
    入口参数：
        name：用户名
        passwd：密码
    返回值：
        cookiestr：返回登陆成功后所构造的cookie
    '''

    url = 'https://passport.baidu.com/v2/?login'
    phantomjsdv = R"/home/cjh/Downloads/phantomjs-2.1.1-linux-x86_64/bin/phantomjs"
    driver = webdriver.PhantomJS(phantomjsdv)
    #driver.maximize_window()
    driver.get(url)
    print('开始登录')
    #进入登陆页面首先显示的是扫码登录，需要先点击扫码登录才能够触发
    #chg_field = driver.find_element_by_class_name('tang-pass-footerBarQrcode').find_element_by_class_name('account-title')
    chg_field = driver.find_element_by_id('TANGRAM__PSP_3__footerULoginBtn')
    chg_field.click()

    name_field = driver.find_element_by_id('TANGRAM__PSP_3__userName')
    name_field.send_keys(name)
    passwd_field = driver.find_element_by_id('TANGRAM__PSP_3__password')
    passwd_field.send_keys(passwd)

    #img_href = driver.find_element_by_id('TANGRAM__PSP_3__verifyCodeImg')
    #print img_href

    login_button = driver.find_element_by_id('TANGRAM__PSP_3__submit')
    login_button.click()

    time.sleep(10)

    #FIXME:理论上会出现一个需要手机验证码的弹出框，所以点击发送然后查看手机能否收到
    #tangram这个id的数字是随机的，一个个试
    for i in range(1, 100):
        
        try:
            sm_code = driver.find_element_by_id('TANGRAM__{}__button_send_mobile'.format(i))
            print sm_code
        except:
            continue

    sm_code.click()
    
    #time.sleep(20)

    #对cookie进行构造，把他的键值对进行重组
    #cookies = driver.get_cookies()
    #print cookies
    #cookiestr = ''
    #for cookie in cookies:
    #    cookiestr = cookiestr + cookie.get('name') + '=' + cookie.get('value') + '; '
    #cookiestr = cookiestr[:-2]
    #print cookiestr
    
    #phantomjs与chromedriver返回的cookie貌似有一些区别
    #return cookies
    #return cookiestr
     
    #暂时先把driver给返回，这里的cookie构造还存在一些问题，可以往后讨论
    #driver.close()
    return driver

def login(name, passwd):

    '''
    模拟登陆贴吧
    入口参数：
        name：用户名
        passwd：密码
    返回值：
        session：登陆过后的session对象，保存着cookie   
    '''
    headers = {
        'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Mobile Safari/537.36'
    }
    #获取登陆成功后的cookie
    cookie = login_cookieget(name, passwd)
    cookies = {
        'Cookie':cookie
    }

    url = 'https://tieba.baidu.com'
    
    #利用session保存
    session = requests.Session()
    response = session.get(url, cookies=cookies, headers=headers).content
    
    return session
    #response = requests.get(url, cookies=cookies, headers=headers).content
    #print response

if __name__ == '__main__':

    login('13587703727', 'cjhcjh19961996')
    #login('18483619375', '13419497653')
