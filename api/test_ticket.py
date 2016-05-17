#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2016/5/17

@author: Jay
"""
import unittest
import urllib2
import json
import threading
import random
import time
from utils.crypto.beiqi_sign import append_url_sign_tk

from beiqissp_test.setting import SERVER_IP, API_SECRET
from beiqissp_test.common.app_login import gen_tk

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class APIETicketTest(unittest.TestCase):
    def test_eticket_check_exist(self):
        code = random.randint(1, 1000000)

        add_url = 'http://{ip}:8300/eticket/add?code={code}'.format(ip=SERVER_IP, code=code)
        add_url = append_url_sign_tk(add_url, gen_tk(), API_SECRET)
        add_res = json.loads(urllib2.urlopen(urllib2.Request(add_url)).read())
        add_status = add_res['status']
        print add_res
        self.assertTrue(add_status == 0)

        check_url = 'http://{ip}:8300/eticket/check?code={code}'.format(ip=SERVER_IP, code=code)
        check_url = append_url_sign_tk(check_url, gen_tk(), API_SECRET)
        print check_url
        check_res = json.loads(urllib2.urlopen(urllib2.Request(check_url)).read())
        print check_res
        check_status = check_res['status']
        self.assertTrue(check_status == 0)

    def test_eticket_check_not_exist(self):
        code = random.randint(1, 1000000)

        check_url = 'http://{ip}:8300/eticket/check?code={code}'.format(ip=SERVER_IP, code=code)
        check_url = append_url_sign_tk(check_url, gen_tk(), API_SECRET)
        print check_url
        check_res = json.loads(urllib2.urlopen(urllib2.Request(check_url)).read())
        print check_res
        check_status = check_res['status']
        self.assertTrue(check_status == 1)

    def test_eticket_check_checked(self):
        code = random.randint(1, 1000000)

        add_url = 'http://{ip}:8300/eticket/add?code={code}'.format(ip=SERVER_IP, code=code)
        add_url = append_url_sign_tk(add_url, gen_tk(), API_SECRET)
        add_res = json.loads(urllib2.urlopen(urllib2.Request(add_url)).read())
        add_status = add_res['status']
        print add_res
        self.assertTrue(add_status == 0)

        check_url = 'http://{ip}:8300/eticket/check?code={code}'.format(ip=SERVER_IP, code=code)
        check_url = append_url_sign_tk(check_url, gen_tk(), API_SECRET)
        print check_url
        check_res = json.loads(urllib2.urlopen(urllib2.Request(check_url)).read())
        print check_res
        check_status = check_res['status']
        self.assertTrue(check_status == 0)

        check_res = json.loads(urllib2.urlopen(urllib2.Request(check_url)).read())
        print check_res
        check_status = check_res['status']
        self.assertTrue(check_status == 3)
