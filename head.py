#!/usr/bin/env python
# -*-coding:utf-8-*-
import  urllib2
import codecs
import sys
import os
import re
import time
reload(sys)
sys.setdefaultencoding('utf-8')
           
#关键字匹配返回值为1,就是找到了;0就是没找到
def IsMatch(filename):
    keyList=["丝","袜","大学生","性感","模","情趣","情人","女友","漂亮","老司机","高跟","腿","摄影","技师"]
    #keyList=["袜","情趣","高跟","腿","3P","双飞","紧身","性感","大学"]
    #keyList=["双飞"]
    #keyList=["模"]
    key_number=0;
    for i in range(len(keyList)):
        if keyList[i].decode('GB2312') in filename:
            key_number+=1
        else:
            key_number+=0
    if(key_number>=1):
        return 1
    else:
        return 0  