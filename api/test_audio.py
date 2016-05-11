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

PUB_BEIQI_MSG_P2P = "BEIQI_MSG_P2P/{sn}"
SUB_BEIQI_MSG_P2P = "BEIQI_MSG_P2P/#"


MQTT_HOST = "112.74.208.65"
MQTT_PORT = 1883

MSG_PAYLOAD = None

class MqttInst(MQTTClient):
    def on_message(self, mqttc, userdata, msg):
        """
        接收到mqtt服务器消息通知
        :param mqttc:
        :param userdata:
        :param msg:
        :return:
        """
        print "msg,",msg
        MSG_PAYLOAD = msg.payload

# GMqttClient = MqttInst()
# GMqttClient.init(MQTT_HOST, MQTT_PORT)
# GMqttClient.subscribe(SUB_BEIQI_MSG_P2P)
#
# # 启动mqtt线程
# mqtt_thread = threading.Thread(target=GMqttClient.start)
# mqtt_thread.setDaemon(True)
# mqtt_thread.start()

class UtilSignTest(unittest.TestCase):
    def test_audio_list(self):
        url = 'http://{ip}:8300/audio/list'.format(ip=SERVER_IP)
        tk = gen_tk()
        url = append_url_sign_tk(url, tk, API_SECRET)

        request = urllib2.Request(url)
        response = urllib2.urlopen(request).read()
        print json.loads(response)


class APIAudioTest(AsyncTestCase):
    def test_pub_2_dev(self):
        url = 'http://{ip}:8300/audio/list'.format(ip=SERVER_IP)
        tk = gen_tk()
        url = append_url_sign_tk(url, tk, API_SECRET)

        request = urllib2.Request(url)
        response = urllib2.urlopen(request).read()
        audio_ls = json.loads(response)

        select_audio = random.choice(audio_ls)

        sn ="PNZHANCHENJIN"

        url = 'http://{ip}:8300/audio/pub_2_dev?dev_sn={sn}&name={name}&ref={ref}'.format(ip=SERVER_IP, sn=sn, name=select_audio['name'], ref=select_audio['ref'])
        tk = gen_tk()
        url = append_url_sign_tk(url, tk, API_SECRET)

        print url

        request = urllib2.Request(url)
        response = urllib2.urlopen(request).read()
        self.wait(MSG_PAYLOAD != None, 5)

        self.assertTrue(MSG_PAYLOAD)

