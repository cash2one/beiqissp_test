#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2016/5/10

@author: Jay
"""
import unittest
import urllib2
import json
import threading
import random
import time
from tornado.testing import AsyncTestCase
from utils.crypto.beiqi_sign import append_url_sign_tk
from py_util.mqtt import MQTTClient

from beiqissp_test.setting import SERVER_IP, API_SECRET
from beiqissp_test.common.app_login import gen_tk

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

PUB_BEIQI_MSG_P2P = "BEIQI_MSG_P2P/{sn}"
SUB_BEIQI_MSG_P2P = "BEIQI_MSG_P2P/#"


MQTT_HOST = "112.74.208.65"
MQTT_PORT = 1883


APIAudioSend2DevTestHdl = None

class MqttInst(MQTTClient):
    def on_message(self, mqttc, userdata, msg):
        if APIAudioSend2DevTestHdl:
            APIAudioSend2DevTestHdl.stop()

GMqttClient = MqttInst()
GMqttClient.init(MQTT_HOST, MQTT_PORT)
GMqttClient.subscribe(SUB_BEIQI_MSG_P2P)

# 启动mqtt线程
mqtt_thread = threading.Thread(target=GMqttClient.start)
mqtt_thread.setDaemon(True)
mqtt_thread.start()


def get_cls():
    url = 'http://{ip}:8300/audio/cls'.format(ip=SERVER_IP)
    url = append_url_sign_tk(url, gen_tk(), API_SECRET)
    return json.loads(urllib2.urlopen(urllib2.Request(url)).read())


def get_album(cls):
    url = "http://{ip}:8300/audio/album?cls={cls}".format(ip=SERVER_IP, cls=urllib2.quote(cls.encode('utf-8')))
    url = append_url_sign_tk(url, gen_tk(), API_SECRET)
    return json.loads(urllib2.urlopen(urllib2.Request(url)).read())


def get_list():
    cls_ls = get_cls()
    print cls_ls
    select_cls = random.choice(cls_ls)['cls']
    album_ls = get_album(select_cls)
    print album_ls
    select_album = random.choice(album_ls)['album']

    url = 'http://{ip}:8300/audio/list?cls={cls}&album={album}'.format(ip=SERVER_IP, cls=urllib2.quote(select_cls.encode('utf-8')), album=urllib2.quote(select_album.encode('utf-8')))
    url = append_url_sign_tk(url, gen_tk(), API_SECRET)

    return json.loads(urllib2.urlopen(urllib2.Request(url)).read())

class APIAudioAudioClsTest(unittest.TestCase):
    def test_audio_list(self):
        self.assertTrue(get_cls())

class APIAudioAudioAlbumTest(unittest.TestCase):
    def test_audio_list(self):
        cls_ls = get_cls()
        select_cls = random.choice(cls_ls)
        self.assertTrue(get_album(select_cls['cls']))

class APIAudioAudioListTest(unittest.TestCase):
    def test_audio_list(self):
        self.assertTrue(get_list())

class APIAudioSend2DevTest(AsyncTestCase):
    def test_pub_2_dev(self):
        audio_ls = get_list()
        select_audio = random.choice(audio_ls)

        sn ="PNZHANCHENJIN"

        url = 'http://{ip}:8300/audio/pub_2_dev?dev_sn={sn}&name={name}&ref={ref}'.format(
            ip=SERVER_IP,
            sn=urllib2.quote(sn),
            name=urllib2.quote(select_audio['name']),
            ref=urllib2.quote(select_audio['ref']))
        url = append_url_sign_tk(url, gen_tk(), API_SECRET)

        urllib2.urlopen(urllib2.Request(url)).read()

        global APIAudioSend2DevTestHdl
        APIAudioSend2DevTestHdl = self
        self.wait(timeout=5)

