#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import
from sqlalchemy import *

metadata = MetaData()

user = Table('user', metadata,
        Column('user_id', String(64), primary_key=True, doc="用户的账号"),
        Column('password', String(64), doc="用户的密码"),
        )

user_tag = Table('user_tag', metadata,
        Column('user_id', String(64), primary_key=True, doc="用户的账号"),
        Column('tag', String(128), doc="用户分析结果标签"),
        )

hot_topic = Table('hot_topic', metadata,
        Column('id', Integer, autoincrement=True, primary_key=True, doc="自增id号"),
        Column('datetime', String(64), doc="热议日期"),
        Column('title', String(64), doc="热议标题"),
        Column('img_path', String(256), doc="分析后热议对应的路径"),
        )
