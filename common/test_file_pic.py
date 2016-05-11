#coding:utf-8
import urllib
from poster.encode import multipart_encode, MultipartParam
from poster.streaminghttp import register_openers
import urllib2
import StringIO
import json
from tornado.httpclient import HTTPRequest, HTTPClient

# 在 urllib2 上注册 http 流处理句柄
register_openers()

file_url="http://api.beiqicloud.com:8106/down?tk=90b21cd88046e516e550a110ec68f703781556a9ec137343c5972c3bc53acc6546ce3e71df6771599f85a9140253b3a767443e3beb9aa27d3bafb725c2647f55084893b7478675190356a93a9a77b4571475bbb5f73feeb83ef684a4a8588c7f28a10d23e729429e113788&r=88ded5a264996f38bf756bc5ca7f932ef339e3a16de2f0689643aecb596b3fb62218c023ba19cc02ac7c774490dc8ff1188c59c4445a8f928dcb67f8a9a3a1196a6e5f889c2bd5ac1ead4b7d7250dd513e9b7c43ec5a0e86cb5e0f5d421cf0fdef08d10006197e47ce64eaeeafa8293e58a61d2c26b0f606b66416d357cdb3beebafb6d3de"

param = MultipartParam(name='media', filename='image.jpg', filetype='image/jpg', fileobj=StringIO.StringIO(urllib2.urlopen(file_url).read()))
datagen, headers = multipart_encode({"media": param})


# 创建请求对象
access_token='fJ_X6EC_A81r_-VseSx0ybDzJon_CUSn9Ns5bggBhuWNCj7LPU7hfY49tFF7FZidUV9-i01bJl7Se0kgTT0HP2fljz-UxQgv3tKUXpat3RogRk8fSlEx0PubW3-Rm0RtXEUbABAMTJ'
type='image'
request = urllib2.Request("http://file.api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=%s"%(access_token, type), datagen, headers)

# 实际执行请求并取得返回
upload_result = urllib2.urlopen(request).read()
upload_result = json.loads(upload_result)
print upload_result


wechat_down_url = "http://file.api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s"%(access_token,upload_result.get('media_id'))
print wechat_down_url
print urllib.urlretrieve(wechat_down_url)


WECHAT_CUSTOMER_SERVICE_URL = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s'
http_client = HTTPClient()
def wechat_customer_response(access_token, payload):
    """
    微信客服反馈
    :param access_token: 访问码
    :param payload:  反馈内容
    :return:
    """
    customer_url = WECHAT_CUSTOMER_SERVICE_URL % access_token
    resp = http_client.fetch(HTTPRequest(customer_url, method='POST', body=json.dumps(payload, ensure_ascii=False)))
    print resp.body


payload = {
        "touser": "oGR4dwERXuGRoHiQnSQyavbM6214",
        "msgtype": "image",
        "image": {
            "media_id": upload_result.get('media_id')
        }
    }

print wechat_customer_response(access_token, payload)