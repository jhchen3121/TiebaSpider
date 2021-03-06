#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

#import domain
#from domain import metadata


# 创建对象的基类:
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    user_id = Column(String(64), primary_key=True, doc="用户的账号")
    password = Column(String(64), doc="用户的密码")


class User_Tag(Base):
    __tablename__ = 'user_tag'
    id = Column(Integer, autoincrement=True, primary_key=True, doc="自增id号")
    user_id = Column(String(64), doc="关联用户表中的user_id")
    user_name = Column(String(64), doc="用户的用户名")
    tag = Column(String(128),doc="用户分析结果标签")

class Hot_Topic(Base):
    __tablename__ = 'hot_topic'
    id = Column(Integer, autoincrement=True, primary_key=True, doc="自增id号")
    datetime = Column(String(64), doc="热议日期")
    title = Column(String(64), doc="热议标题")
    img_path = Column(String(256), doc="图片路径")

class Celery_TaskId(Base):
    __tablename__ = 'celery_taskid'
    id = Column(Integer, autoincrement=True, primary_key=True, doc="自增id号")
    task_name = Column(String(64), doc="任务名，用于区分是爬虫还是模拟登陆模块")
    task_id = Column(String(64), doc="celery任务对应的id号")

if __name__ == '__main__':
    DB_URL = 'mysql+pymysql://tbspider:tbspider@127.0.0.1/tbspiderdb?charset=utf8'
    engine = create_engine(DB_URL)
    Base.metadata.create_all(engine)
