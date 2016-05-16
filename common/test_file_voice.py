#coding:utf-8
import urllib
from poster.encode import multipart_encode, MultipartParam
from poster.streaminghttp import register_openers
import urllib2
import StringIO
import json

# 在 urllib2 上注册 http 流处理句柄
register_openers()


file_url="http://api.beiqicloud.com:8106/down?tk=90bd3b909b189374e001e3648e00b2741a4c49e836c011268ac4686ebd3cce6745ae25ad7b3c316ea7bd9d233566879253740f0ddca8954a15c5c742c2647f55084893b7478675190356a93a9a77b4571475bbb5f73feeb83ef6fccd&r=c8d1da852c82314edd703a87be1dfb6b845bbab1f5417a164d0b85654b198b3b0ed7d2ab6795a5d8af52dd70fe0142a2afd9c8b499ddd8706a91d6a02b28a80e57586dbfa413e19b29987f484660ec6709a94b74c2307ee1cb5e0f5d421cf0fdef08d10006197e"

param = MultipartParam(name='media', filename='voice.amr', filetype='voice/amr', fileobj=StringIO.StringIO(urllib2.urlopen(file_url).read()))
datagen, headers = multipart_encode({"media": param})


# 创建请求对象
access_token='HJU1NES0x1xnYjnqeVDB8Xb0A7ld-GptIUs-Ppp1eSq1kYG4BOVt5dGjl0zOctX7__EJXmpxFOE2gKLMAIW4O0PPvCnKs_PGfti5j0wnmdEBZgctfdzYFrLgjlaPgEAnNWZiADAAJM'
type='voice'
request = urllib2.Request("http://file.api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=%s"%(access_token, type), datagen, headers)

# 实际执行请求并取得返回
upload_result = urllib2.urlopen(request).read()
upload_result = json.loads(upload_result)
print upload_result


wechat_down_url = "http://file.api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s"%(access_token,upload_result.get('media_id'))
print wechat_down_url
print urllib.urlretrieve(wechat_down_url, "d:\test.amr")