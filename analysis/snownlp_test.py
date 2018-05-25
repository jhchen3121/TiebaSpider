#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import
import codecs
import re
import numpy as np
import pymysql
from snownlp import SnowNLP
import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt
from snownlp import sentiment
from snownlp.sentiment import Sentiment

comment = []
with open(u'/home/cjh/Desktop/TiebaSpider/data/hottopic_data/2018-01-26/解忧杂货店.txt', mode='r', encoding='utf-8') as f:
    rows = f.readlines()
    for row in rows:
        if row not in comment:
            comment.append(row.strip('\n'))
def snowanalysis(self):
    sentimentslist = []
    for li in self:
        print(li)
        s = SnowNLP(li)
        print(s.sentiments)
        sentimentslist.append(s.sentiments)
    plt.hist(sentimentslist, bins=np.arange(0, 1, 0.01))
    plt.show()
    plt.savefig('/home/cjh/test.png')
snowanalysis(comment)
