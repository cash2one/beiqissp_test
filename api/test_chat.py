#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2016/5/14

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

PUB_BEIQI_MSG_BCAST = "BEIQI_MSG_BCAST/{gid}"
SUB_BEIQI_MSG_BCAST = "BEIQI_MSG_BCAST/#"


MQTT_HOST = "112.74.208.65"
MQTT_PORT = 1883


APIChatMsgBcastTestHdl = None

class MqttInst(MQTTClient):
    def on_message(self, mqttc, userdata, msg):
        if APIChatMsgBcastTestHdl:
            APIChatMsgBcastTestHdl.stop()

GMqttClient = MqttInst()
GMqttClient.init(MQTT_HOST, MQTT_PORT)
GMqttClient.subscribe(SUB_BEIQI_MSG_BCAST)

# 启动mqtt线程
mqtt_thread = threading.Thread(target=GMqttClient.start)
mqtt_thread.setDaemon(True)
mqtt_thread.start()

class APIChatMsgBcastTest(AsyncTestCase):
    def test_chat_msg_bcast(self):
        file_type = "3"
        fn = "yT08JbAAQP3zcrAscxJ0-F0QjYhYy06PRre1jD-5B6_GJaV1gt1uzE9ELYQmPJcG.amr"
        ref = "88ded5a264996f38881538c1bf47be6cce05deb04dd5cd0eb359b8ea6d1f3dd27f5fc023ba19cc35cc2f7331a8f1cdcc24b148e47367e9b797dd46ccdda1c5442d21398f9c5983da68c92f7b3c039e267aca333ef21d38d19a3456351b65c0cbbf5aa36537733a6afb26dcb1e8e2486869c1691d53cab33ff3284f823a9df9ddac81d7beac"

        url = 'http://{ip}:8300/chat/bcast?file_type={ftype}&fn={fn}&ref={ref}'.format(
            ip=SERVER_IP,
            ftype=urllib2.quote(file_type),
            fn=urllib2.quote(fn),
            ref=urllib2.quote(ref))
        url = append_url_sign_tk(url, gen_tk(), API_SECRET)
        print url

        urllib2.urlopen(urllib2.Request(url)).read()

        global APIChatMsgBcastTestHdl
        APIChatMsgBcastTestHdl = self
        self.wait(timeout=5)

