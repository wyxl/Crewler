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
           
#�ؼ���ƥ�䷵��ֵΪ1,�����ҵ���;0����û�ҵ�
def IsMatch(filename):
    keyList=["˿","��","��ѧ��","�Ը�","ģ","��Ȥ","����","Ů��","Ư��","��˾��","�߸�","��","��Ӱ","��ʦ"]
    #keyList=["��","��Ȥ","�߸�","��","3P","˫��","����","�Ը�","��ѧ"]
    #keyList=["˫��"]
    #keyList=["ģ"]
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