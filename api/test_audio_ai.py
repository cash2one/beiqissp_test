#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2016/5/20

@author: Jay
"""
import time
import unittest
import urllib2
import json
from py_util.interfaces.file import up_beiqi_file, down_beiqi_file
from beiqissp_test.setting import TEST_USER_NAME,SERVER_IP,API_SECRET
from utils.crypto.beiqi_sign import append_url_sign_tk
from beiqissp_test.common.app_login import gen_tk
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class APIAudioAudioAITest(unittest.TestCase):
    def test_audio_ai(self):
        wav_file= r"C:\Users\151117a\Desktop\res\iflytek02.wav".decode('utf8')
        file_object = open(wav_file, 'rb')
        file_data = file_object.read()
        fn = wav_file.split('\\')[-1]
        print "fn,",fn
        print len(file_data)
        stime = time.time()
        beiqi_ref = up_beiqi_file(TEST_USER_NAME, 3, fn, file_data, 'http://{ip}:8106/up?'.format(ip=SERVER_IP))
        print "beiqi_ref,",beiqi_ref

        ai_url = 'http://{ip}:8300/audio/ai?fn={fn}&ref={ref}'.format(ip=SERVER_IP,fn=fn, ref=urllib2.quote(beiqi_ref))
        ai_url = append_url_sign_tk(ai_url, gen_tk(), API_SECRET)
        print "ai_url,",ai_url

        resp = urllib2.urlopen(urllib2.Request(ai_url)).read()
        resp = json.loads(resp)

        etime = time.time()
        print "diff time:%s" % (etime - stime)
        print "resp,",resp

        ai_data = down_beiqi_file(TEST_USER_NAME, resp['fn'], resp['ref'], 'http://%s:8106/down?tk={tk}&r={ref}'% SERVER_IP)
        mp3file = r"C:\Users\151117a\Desktop\res\%s" % resp['fn']
        print mp3file
        file_object = open(mp3file, 'wb')
        file_object.write(ai_data)
        file_object.close()

        etime = time.time()
        print "diff time:%s" % (etime - stime)
        print "resp,",resp

    def test_audio_ai_new(self):
        wav_file= r"C:\Users\151117a\Desktop\res\iflytek02.wav".decode('utf8')
        fn = "%s.wav"%int(time.time())
        file_object = open(wav_file, 'rb')
        file_data = file_object.read()

        stime = time.time()
        ai_url = 'http://{ip}:8200/audio_ai'.format(ip=SERVER_IP)
        print "ai_url,",ai_url

        res = urllib2.urlopen(urllib2.Request(ai_url, data=file_data))
        print res.headers
        resp = res.read()

        etime = time.time()
        print "diff time:%s" % (etime - stime)

        mp3file = r"C:\Users\151117a\Desktop\res\%s" % fn
        print mp3file
        file_object = open(mp3file, 'wb')
        file_object.write(resp)
        file_object.close()

        etime = time.time()
        print "diff time:%s" % (etime - stime)