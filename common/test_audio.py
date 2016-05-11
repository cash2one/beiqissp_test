#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2016/5/9

@author: Jay
"""

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import audioread

filename = r"C:\Users\151117a\Desktop\资源\林志炫-没离开过.wav"
print filename
filename = filename.decode('utf8')
print filename
f = audioread.audio_open(filename)
print f.__dict__
print (f.channels, f.samplerate, f.duration)


filename = r"C:\Users\151117a\Desktop\资源\红色娘子军连歌.mp3"
print filename
filename = filename.decode('utf8')
print filename
f = audioread.audio_open(filename)
print (f.channels, f.samplerate, f.duration)

filename = r"C:\Users\151117a\Desktop\资源\dow.amr"
print filename
filename = filename.decode('utf8')
print filename
f = audioread.audio_open(filename)
print (f.channels, f.samplerate, f.duration)