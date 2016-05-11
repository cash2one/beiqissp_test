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

file_url="http://api.beiqicloud.com:8106/down?tk=90b21cd88046e516e550a110ec68f703781556a9ec137343c5972c3bc53acc6546ce3e7be4352d3edefec7696724c8fe2b054c5996c1a03c38f29830965c050f5a01a18403d70c6e301afe0dac22f31b521dcbf7be73ace272b8ea90fd02e32078d2491682072fee253489&r=88ded5a264996f38bf756bc5ca7f932ef339e3a16de2f0689643aecb596b3fb62218c023ba19cc02ac7c774490dc8ff1188c59c4445a8f928dcb67f8a9a3a1196a3c03efdd50bbd17bda30243e11af3343c07e02ef0721939f6675071055c2ceab59a87735552970f831ada2e9c0597c11ea5f766afe9832e33e798c07bef78b8e81dba3ea"

param = MultipartParam(name='media', filename='video.mp4', filetype='video/mp4', fileobj=StringIO.StringIO(urllib2.urlopen(file_url).read()))
datagen, headers = multipart_encode({"media": param})


# 创建请求对象
access_token='MP5AIQkgKPqmyszI6YPmfHSHb1lP7UAdivzmPX24c2T3bRKNJpxEiuzGm5AkrGTKypUl8r1UtrSuh-Lkr_auerfXmDZSYByoX8Eyjd2e-nKKloMvjva8V7L6pYzQfFvzGVTfAJAVKI'
type='video'
request = urllib2.Request("http://file.api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=%s"%(access_token, type), datagen, headers)

# 实际执行请求并取得返回
upload_result = urllib2.urlopen(request).read()
upload_result = json.loads(upload_result)
print upload_result


wechat_down_url = "http://file.api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s"%(access_token,upload_result.get('media_id'))
print wechat_down_url
print urllib.urlretrieve(wechat_down_url, "d:\test.amr")


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
        "msgtype": "video",
        "voice": {
            "media_id": upload_result.get('media_id'),
            "thumb_media_id": "thumb_media_id",
            "title": "title",
            "description":"description"
        }
    }

print wechat_customer_response(access_token, payload)