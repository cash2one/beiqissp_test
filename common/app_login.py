#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2016/5/10

@author: Jay
"""
import urllib2
import site, os; site.addsitedir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))));site.addsitedir(os.path.dirname(os.path.dirname(os.path.realpath(__file__))));site.addsitedir(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), "beiqissp"))
from beiqissp_test.setting import SERVER_IP, TEST_USER_NAME, API_KEY, TEST_PASSWD


sso_gentk_url = 'http://{ip}:8104/gen_tk?api_key={api_key}&username={user_name}&pwd={passwd}'.format(ip=SERVER_IP, api_key=API_KEY, user_name=TEST_USER_NAME, passwd=TEST_PASSWD)


def gen_tk():
    headers = {"user-agent":"okhttp/2.2.0"}
    request = urllib2.Request(sso_gentk_url)
    request.add_header("user-agent", "okhttp/2.2.0")
    response = urllib2.urlopen(request)
    return response.read()

print gen_tk()
