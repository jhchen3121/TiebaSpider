# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import
from lxml import etree
import requests
import sys

from login import login_selenium
#from login import login
from msgget import build_url
from msgget import hot_mesg_get
from msgget import user_mesg_get
from msgget import get_agent_ip

#reload(sys)
#sys.setdefaultencoding('utf8')

#每条热议对应的url
#url = 'https://tieba.baidu.com/mo/q/hotMessage?topic_id={}&topic_name={}'.format('229808', '英雄联盟年度颁奖盛典')
#url = 'http://tieba.baidu.com/hottopic/browse/hottopic?topic_name={}'

if __name__ == '__main__':

    #base_url = 'https://tieba.baidu.com/mo/q/hotMessage/list'

    topic_url_list, title_list = build_url.buildurl()

    #print topic_url_list, title_list

    hot_mesg_get.tile_url_get(topic_url_list, title_list)

    #login_selenium.login('13587703727', 'cjhcjh19961996')
    
    #user_mesg_get.user_name_get('13587703727', 'cjhcjh19961996')

    #user_mesg_get.tieba_concern_get('13587703727', 'cjhcjh19961996')

    #user_mesg_get.personal_tiezi_get('13587703727', 'cjhcjh19961996')
    #user_mesg_get.personal_tiezi_get('15165527699', 'yueyue.100329')

    #proxies = get_agent_ip.choose_proxies()
    #print proxies
