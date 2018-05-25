#!/bin/bash

#开启20个异步的线程进行来进行贴吧的热议趴取
celery -A workers worker -c 20 -l info
