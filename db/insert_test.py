#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
from table_db_create import User, User_Tag, Hot_Topic
import time

if __name__ == '__main__':

    DB_URL = 'mysql+pymysql://tbspider:tbspider@127.0.0.1/tbspiderdb?charset=utf8'
    engine = create_engine(DB_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    user = User()
    user_tag = User_Tag()
    hot_topic = Hot_Topic()

    user.user_id = "13587703727"
    user.password = "cjhcjh19961996"
    session.add(user)

    user_tag.user_id = "13587703727"
    user_tag.tag = "一二三"
    session.add(user_tag)

    hot_topic.datetime = time.time()
    hot_topic.title = "康师傅绿色食品"
    hot_topic.keywords = "健康"
    session.add(hot_topic)

    session.commit()
