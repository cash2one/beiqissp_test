#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2016/5/16

@author: Jay
"""
from tornado.httpclient import HTTPClient
from tornado.httpclient import HTTPRequest
import site, os; site.addsitedir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))));site.addsitedir(os.path.dirname(os.path.dirname(os.path.realpath(__file__))));site.addsitedir(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), "beiqissp"))
print os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
from py_util.filetoken import gen_file_tk
import sys
print sys.path
import urllib
from poster.encode import multipart_encode, MultipartParam
from poster.streaminghttp import register_openers
import urllib2
import StringIO
import json

# 在 urllib2 上注册 http 流处理句柄
register_openers()

from beiqissp_test.setting import SERVER_IP, TEST_USER_NAME
http_client = HTTPClient()


up_file_url = 'http://{ip}:8106/up?'.format(ip=SERVER_IP)


def beiqi_file_up(mp3_path, fn):
    tk = gen_file_tk(TEST_USER_NAME, fn, 1, 0)
    print "tk,",tk

    file_type = 3
    up_args = {'tk': tk, 'src': file_type, 'by': TEST_USER_NAME, 'usage': 'share'}
    file_object = open(mp3_path, 'rb')

    data = file_object.read()
    file_object.close()
    print len(data)

    url = up_file_url + urllib.urlencode(up_args)
    print "url,",url
    resp = http_client.fetch(HTTPRequest(url, method='POST', body=data))
    return json.loads(resp.body)


def beiqi_file_down(fn, ref):
    acc = "18610060484@jiashu.com"
    tk = gen_file_tk(acc, fn, 0, 0)
    down_file_url = 'http://{ip}:8106/down?'.format(ip=SERVER_IP)
    pic_url = down_file_url + urllib.urlencode({'tk': tk, 'r': ref})
    return pic_url


access_token='HJU1NES0x1xnYjnqeVDB8Xb0A7ld-GptIUs-Ppp1eSq1kYG4BOVt5dGjl0zOctX7__EJXmpxFOE2gKLMAIW4O0PPvCnKs_PGfti5j0wnmdEBZgctfdzYFrLgjlaPgEAnNWZiADAAJM'
def wechat_file_up(beiqi_down_ful, fn):
    file_type_flag = fn.split('.')[-1]
    filetype='voice/%s' % (file_type_flag)
    print "filetype,",filetype
    param = MultipartParam(name='media', filename=fn, filetype=filetype, fileobj=StringIO.StringIO(urllib2.urlopen(beiqi_down_ful).read()))
    datagen, headers = multipart_encode({"media": param})
    print "datagen,",datagen
    print "headers,",headers

    # 创建请求对象
    type='voice'
    request = urllib2.Request("http://file.api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=%s"%(access_token, type), datagen, headers)

    # 实际执行请求并取得返回
    upload_result = urllib2.urlopen(request).read()
    return json.loads(upload_result)

def wechat_file_down(media_id):
    wechat_down_url = "http://file.api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s"%(access_token, media_id)
    print "wechat_down_url,",wechat_down_url
    print urllib.urlretrieve(wechat_down_url)



mp3_path = r"C:\Users\151117a\Desktop\资源\down.mp3".decode('utf8')
fn = str(mp3_path.split('\\')[-1])

up_res = beiqi_file_up(mp3_path, fn)
beiqi_down_url = beiqi_file_down(fn, up_res['r'])
print "beiqi_down_url,",beiqi_down_url
wechat_up_res = wechat_file_up(beiqi_down_url, fn)
print "wechat_up_res,",wechat_up_res
wechat_down_res = wechat_file_down(wechat_up_res['media_id'])
print wechat_down_res

