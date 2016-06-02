#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2016/6/2

@author: Jay
"""
import unittest
import urllib2
from beiqissp_test.setting import SERVER_IP
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class APILocationTest(unittest.TestCase):
    def test_get_location(self):
        param = {
            "accesstype": 1,
            "imei": "355440073090762",
            "smac": "C0:CC:F8:E7:E2:C5",
            "macs": "00:0C:43:30:92:00,-45,NS3000G|D4:EE:07:39:BA:12,-65,ZuiPin-AP04|C0:A0:BB:F7:7C:58,-64,huiming",
        }
        loc_url = 'http://{ip}:8202/location'.format(ip=SERVER_IP) + "?" + "&".join("%s=%s"%(k, urllib2.quote(str(v))) for k, v in param.items())
        print loc_url
        resp = urllib2.urlopen(urllib2.Request(loc_url)).read()
        print resp