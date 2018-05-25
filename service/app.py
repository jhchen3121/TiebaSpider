#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import
from flask import Flask,Response
from flask import send_file
from flask import jsonify
from flask import request

from msgget import build_url
from msgget import hot_mesg_get
from msgget import user_mesg_get
from msgget import get_agent_ip

from analysis import user_tag_analysis

from celery.result import AsyncResult
from workers import app_celery
from tasks import celery_hottopic_spider
from tasks import celery_login_tieba

from util import db
from io import BytesIO

import os
import json
import time

app = Flask(__name__)
app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))

#全局用户账号
id = None

#注册需要用到的js以及css
@app.route('/bootstrap-datetimepicker.min.js')
def datetimepickerjs():
    return send_file("/home/cjh/Desktop/TiebaSpider/web/bootstrap-datetimepicker.min.js")
@app.route('/bootstrap-datetimepicker.min.css')
def datetimepickercss():
    return send_file("/home/cjh/Desktop/TiebaSpider/web/bootstrap-datetimepicker.min.css")
@app.route('/jquery_timer.js')
def jquery_timer():
    return send_file("/home/cjh/Desktop/TiebaSpider/web/jquery_timer.js")

#加载登陆静态页面
@app.route('/login')
def login_html():
    return send_file("/home/cjh/Desktop/TiebaSpider/web/login.html")

@app.route('/login_post', methods=['GET', 'POST'])
def login_post():
    #如果正确，返回code=0，前端跳转至message页面
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #如果能在数据库中查询到对应的帐号密码，则成功
        result = db.user_check(username, password)

        if result:
            #把账号存储至全局
            global id
            id = username
            return jsonify(code=0, resason="登录成功")
        else:
            return jsonify(code=-1002, reason="帐号密码错误")

#加载注册静态页面
@app.route('/register')
def register_html():
    return send_file("/home/cjh/Desktop/TiebaSpider/web/register.html")

#加载显示静态页面
@app.route('/mesgshow')
def mesgshow_html():
    return send_file("/home/cjh/Desktop/TiebaSpider/web/mesgshow.html")

#加载爬虫工具静态页面
@app.route('/spider_tools')
def spider_tools():
    return send_file("/home/cjh/Desktop/TiebaSpider/web/spider_tools.html")


@app.route('/send_sm_code')
def send_sm_code():
    #获取前端发送的手机号，生成对应的验证码，调用接口
    return True

#注册页面表单信息的提交
@app.route('/register_post', methods=['POST', 'GET'])
def register_post():
    #先进行验证码的校验，然后插入数据库
    #若数据库中不存在对应的信息，正常插入，返回code=0，前端页面跳转
    if request.method == 'POST':
        username =  request.form['username']
        password = request.form['userpwd']
        confirm = request.form['confirm']
        sm_code = request.form['sm_code']

        if password != confirm:
            return jsonify(code=-1000, reason="密码输入不一致")
        if sm_code != '1234':
            return jsonify(code=-1001, reason="验证码错误")
        
        #把username以及password插入至数据库
        db.user_insert(username, password)
        return jsonify(code=1,reason="注册成功")

#内容展示页面
@app.route('/message_show_post', methods=['POST', 'GET'])
def message_show_post():

    if request.method == 'POST':
        date = request.form['date']
        if not date:
            return jsonify(code=-1, reason='无数据')
        #重新把date的2018-3-3构造成2018-03-03
        #此处可以用join的方法拼接
        date = date.split('-')
        if len(date[1]) == 1:
            date[1] = '0' + date[1]
        if len(date[2]) == 1:
            date[2] = '0' + date[2]
        date = date[0] + '-' + date[1] + '-' + date[2]
        #print date
        #查询数据库中的对应日期的热议
        result = db.hottopic_search(str(date))
        #print result
        #利用jsonify把unicode转化成中文格式
        if result:
            return jsonify(code=0, result=result)
        
        return jsonify(code=-1, reason="无图片")

#给前端显示对应的图片内容
@app.route('/img_show', methods=['POST', 'GET'])
def img_show():
    title = request.args.get('title')
    datetime = request.args.get('date')

    img_path = "/home/cjh/Desktop/TiebaSpider/data/analysis_data/{date}/{title}.jpg".format(date=datetime, title=title)

    image = file(img_path)

    resp = Response(image, mimetype="image/jpeg")
    return resp

#前端检测celery的运行状态,用于控制爬虫按钮开启关闭
@app.route('/celery_task_status')
def celery_task_status():

    #从本地数据库中获取对应的task_id号
    task_id_list = db.celery_task_id_search('spider')

    if task_id_list:
        for each_id in task_id_list:
            each_task_state = celery_hottopic_spider.AsyncResult(each_id)

            each_task_state = each_task_state.state
            print each_task_state
            #如果还存在一个进行中，就说明还在执行
            #状态分别为PENDING,SUCCESS两种
            if each_task_state == 'PENDING':
                return jsonify(code=0, reason="进行中")

        #然后在删除表中字段
        db.celery_task_id_delete('spider')

        return jsonify(code=0, reason="未进行")
    else:
        return jsonify(code=0, reason="未进行")

#检测爬虫抓取的状态，用于给前端进度条显示
@app.route('/celery_spider_prog')
def celery_spider_prog():
    #从本地数据库中获取对应的task_id号
    task_id_list = db.celery_task_id_search('spider')

    if task_id_list:

        success_count = 0
        for each_id in task_id_list:
            each_task_state = celery_hottopic_spider.AsyncResult(each_id)
            each_task_state = each_task_state.state
            
            #result_list.append(each_task_state)
            #返回成功的个数
            if each_task_state != 'PENDING':
                success_count += 1
    
    return jsonify(code=0, reason=success_count)

#前端爬虫开启按钮
@app.route('/begin_tieba_spider')
def begin_tieba_spider():
    '''
    收到请求后开启后台爬虫
    '''
    #把所有的并发task_id构成一个list，查询每一个的状态，直到全部完成
    task_id_list = []

    topic_url_list, title_list = build_url.buildurl()

    for url, each_title in zip(topic_url_list, title_list):
        task_result = app_celery.send_task('tasks.celery_hottopic_spider', args=(url, each_title,))
        task_id_list.append(task_result.id)

    #把对应的task_id插入本地数据库
    db.celery_task_id_inster('spider', task_id_list)
    print '插入成功'

    #返回正在执行的task_id，可以让前端知道爬虫是否正在执行
    return jsonify(code=0, reason="爬虫开启成功，关注后台日志", task_id_list=task_id_list)

#根据热议生成词云
@app.route('/build_wdcloud')
def build_wdcloud():

    #此处调用shell脚本，因为是需要执行python3的操作
    shell_file_path = os.environ['PROJ_DIR'] + '/build_wdcolud_pic.sh'

    os.system('sh {}'.format(shell_file_path))

    return jsonify(code=0, reason="词云生成成功")

#舆情分析
@app.route('/build_snownlp')
def build_snownlp():
    #分析的是当日的结果
    #此处调用shell脚本，因为是需要执行python3的操作
    shell_file_path = os.environ['PROJ_DIR'] + '/sentiment_analysis_pic.sh'

    os.system('sh {}'.format(shell_file_path))

    return jsonify(code=0, reason="成功")

#舆情分析图片显示
@app.route('/show_snownlp_pic')
def show_snownlp_pic():

    datetime = time.strftime("%Y-%m-%d", time.localtime())
    img_path = os.environ['PROJ_DIR'] + '/data/analysis_data/{date}/sentiments.jpg'.format(date=datetime)

    image = file(img_path)

    resp = Response(image, mimetype="image/jpeg")
    return resp

#检测舆情分析是否已经存在结果
@app.route('/check_snownlp')
def check_snownlp():
    '''
    检查本地是否已经分析过存在对应的文件
    '''

    datetime = time.strftime("%Y-%m-%d", time.localtime())
    path = u'/home/cjh/Desktop/TiebaSpider/data/analysis_data/{}/{}'.format(datetime, 'sentiments.jpg')

    if os.path.exists(path):
        return jsonify(code=0, reason="存在")
    else:
        return jsonify(code=-1, reason="不存在")

#贴吧模拟登陆url
#FIXME
#需要结合celery进行异步处理
@app.route('/tieba_login', methods=['POST', 'GET'])
def user_msg_get():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        #input后台测试，获取验证码,测试完毕input有效
        #sm_code = input('请输入获取到的验证码:')

        #print sm_code
        #task_result = app_celery.send_task('tasks.celery_login_tieba', args=(username, password, ))
        #task_result_id = task_result.id

        #把对应的task_id插入本地数据库
        #db.celery_task_id_inster('login', task_result_id)

        #FIXME:就不要用异步登陆了，直接把id以及内容先写入数据库
        #txt_path = user_mesg_get.personal_tiezi_get(username, password)
        #TODO:把id跟分析结果一起存入数据库
        filepath = '/home/cjh/Desktop/TiebaSpider/data/user_data/庆余年◆.txt'
        user_name, tag = user_tag_analysis.analyse_user_tag(filepath)

        global id
        
        db.user_tag_insert(id, user_name, tag)

        return jsonify(code=0, reason="开始模拟登陆", user_id=id)

@app.route('/user_tag_get')
def user_tag_get():
    
        
    global id
    user_id = id

    result = db.user_tag_select(user_id)

    return jsonify(code=0, result=result)

#检查模拟登陆状态，前端请求接口
@app.route('/tieba_login_status')
def tieba_login_status():

    #从本地数据库中获取对应的task_id号
    task_id = db.celery_task_id_search('login')

    if task_id:
    
        task_id = task_id[0][0]
        if task_id:
            task_status = celery_login_tieba.AsyncResult(task_id)
            task_status = task_status.state
            
            if task_status == 'PENDING':
                return jsonify(code=1, reason="正在登陆")
            elif task_status == 'SUCCESS':
                #然后在删除表中字段
                db.celery_task_id_delete('login')

                #FIXME:需要给前端返回一些字段，用户名，关注的贴吧，还有所发的帖子等，最后生成的关键字都需要一个返回的方法
                return jsonify(code=0, reason="登陆完毕")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
