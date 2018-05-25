# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
import sys
sys.path.append(r"/home/cjh/Desktop/TiebaSpider/util")
from table_db_create import User, User_Tag, Hot_Topic, Celery_TaskId
import time

#用户表数据插入
def user_insert(username, password):
    '''
    把前端发送注册用户表单插入数据库
    入口参数:
        username:用户名
        password:密码
    '''

    DB_URL = 'mysql+pymysql://tbspider:tbspider@127.0.0.1/tbspiderdb?charset=utf8'
    engine = create_engine(DB_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    user = User()
    user.user_id = username
    user.password = password

    session.add(user)
    session.commit()


#查询用户表内容是否匹配
def user_check(username, password):
    '''
    检验登陆表单内容能否在数据库中查询出来
    入口参数:
        username:用户名
        password:密码
    返回值:
        result:返回是否查询到的结果
    '''

    DB_URL = 'mysql+pymysql://tbspider:tbspider@127.0.0.1/tbspiderdb?charset=utf8'
    engine = create_engine(DB_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(User).filter(User.user_id == username).filter(User.password == password).all()

    if query:
        return True
    else:
        return False

#热议时间，标题，图片路径插入
def hottopic_inster(date, title, img_path):
    '''
    把时间热议名以及分析好的词云图片的路径插入至数据库中
    入口参数：
        date:热议日期
        title:热议标题
        img_path:图片路径
    '''

    DB_URL = 'mysql+pymysql://tbspider:tbspider@127.0.0.1/tbspiderdb?charset=utf8'
    engine = create_engine(DB_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    hot_topic = Hot_Topic()
    hot_topic.datetime = date
    hot_topic.title = title
    hot_topic.img_path = img_path

    session.add(hot_topic)
    session.commit()

#热议内容查询
def hottopic_search(date):
    '''
    根据时间的入口查询出记录
    入口参数：
        date:热议日期
    返回值：
        items：字典格式的表格字段
    '''
    items = []
    DB_URL = 'mysql+pymysql://tbspider:tbspider@127.0.0.1/tbspiderdb?charset=utf8'
    engine = create_engine(DB_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    hot_topic = Hot_Topic()

    query = session.query(Hot_Topic).filter(Hot_Topic.datetime == date).all()

    if query:
        #转化为字典格式
        items = [to_dict(i.__dict__) for i in query]
        return items
    else:
        return None

def celery_task_id_inster(task_name, task_id_list):
    '''
    异步任务task_id号的插入本地数据库
    入口参数：
        task_name:用于区分任务名
        task_id_list:存放task_id的列表
    '''

    DB_URL = 'mysql+pymysql://tbspider:tbspider@127.0.0.1/tbspiderdb?charset=utf8'
    engine = create_engine(DB_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    if task_name == 'spider':
        for i in task_id_list:
            celery_taskid = Celery_TaskId()
            celery_taskid.task_name = task_name
            celery_taskid.task_id = i

            session.add(celery_taskid)
            session.commit()
    else:
        celery_taskid = Celery_TaskId()
        celery_taskid.task_name = task_name
        celery_taskid.task_id = task_id_list

        session.add(celery_taskid)
        session.commit()

def celery_task_id_search(task_name):
    '''
    从本地数据库中查询出对应的task_id
    '''

    DB_URL = 'mysql+pymysql://tbspider:tbspider@127.0.0.1/tbspiderdb?charset=utf8'
    engine = create_engine(DB_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(Celery_TaskId.task_id).filter(Celery_TaskId.task_name == task_name).all()

    if task_name == 'spider':
        task_id_list = [i[0] for i in query]
    else:
        return query

    return task_id_list


def celery_task_id_delete(task_name):
    '''
    删除已经完成的task_id
    '''

    DB_URL = 'mysql+pymysql://tbspider:tbspider@127.0.0.1/tbspiderdb?charset=utf8'
    engine = create_engine(DB_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Celery_TaskId).filter(Celery_TaskId.task_name == task_name).delete()
    session.commit()

def user_tag_insert(user_id, user_name, tag):
    '''
    分析后用户标签的插入
    '''

    DB_URL = 'mysql+pymysql://tbspider:tbspider@127.0.0.1/tbspiderdb?charset=utf8'
    engine = create_engine(DB_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    #若已存在相同的user_name，执行update
    #FIXME
    user_tag = User_Tag()
    user_tag.user_id = user_id
    user_tag.user_name = user_name
    user_tag.tag = tag

    session.add(user_tag)
    session.commit()

def user_tag_select(user_id):
    '''
    查询
    '''
    DB_URL = 'mysql+pymysql://tbspider:tbspider@127.0.0.1/tbspiderdb?charset=utf8'
    engine = create_engine(DB_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    #select all
    query = session.query(User_Tag).filter(User_Tag.user_id == user_id).all()
    
    query_list = [to_dict(i.__dict__) for i in query]

    return query_list

def to_dict(query):

    d = dict()
    #hottopic的字典类型
    d['id'] = query.get('id')
    d['datetime'] = query.get('datetime')
    d['title'] = query.get('title')
    d['img_path'] = query.get('img_path')

    #user_tag字典类型
    d['user_id'] = query.get('user_id')
    d['user_name'] = query.get('user_name')
    d['tag'] = query.get('tag')

    return d

