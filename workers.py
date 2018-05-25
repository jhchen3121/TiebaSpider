#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

from celery import Celery

#app_celery = Celery('task', include=['tasks'])
app_celery = Celery('tasks', backend='amqp', broker='amqp://guest@localhost//')

app_celery.conf.update(
    CELERY_TIMEZONE='Asia/Shanghai',
    CELERY_ENABLE_UTC=True,
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
    CELERY_IMPORTS = ("tasks",),
)
