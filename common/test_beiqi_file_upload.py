#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2016/5/10

@author: Jay
"""
from tornado.httpclient import HTTPClient
from tornado.httpclient import HTTPRequest
import site, os; site.addsitedir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))));site.addsitedir(os.path.dirname(os.path.dirname(os.path.realpath(__file__))));site.addsitedir(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), "beiqissp"))
print os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
import urllib
from py_util.filetoken import gen_file_tk
import sys
print sys.path

from beiqissp_test.setting import SERVER_IP, TEST_USER_NAME
http_client = HTTPClient()


up_file_url = 'http://{ip}:8106/up?'.format(ip=SERVER_IP)

fn = "test.mp3"
tk = gen_file_tk(TEST_USER_NAME, fn, 1, 0)

print "tk,",tk

file_type = 3
up_args = {'tk': tk, 'src': file_type, 'by': TEST_USER_NAME, 'usage': 'share'}


mp3file= r"C:\Users\151117a\Desktop\资源\Sleep Away.mp3".decode('utf8')
file_object = open(mp3file)

resp = http_client.fetch(HTTPRequest(up_file_url + urllib.urlencode(up_args), method='POST', body=file_object.read()))
print resp.body