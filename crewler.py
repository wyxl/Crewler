#!/usr/bin/env python
# -*-coding:utf-8-*-
import  urllib2
import codecs
import os
import re
import time
import head
from lxml import etree
from os import system
from selenium import webdriver
header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
            , "Connection": "keep-alive"
         }
                   
browser = webdriver.Chrome()
browser.set_window_size(0,0)
time.sleep(2)      

#ȫ�ֱ���
URL="https://t66y.com/thread0806.php?fid=16&search=&page="
SavePath="E:\python\cl\mm\\"

#Function1 ������ҳ��ַ�����ÿһҳ�ĵ�ַ,����չ
def GetPageAddr():
    for Pagenum in range(1,101):
        GetPageItems(Pagenum)   

#Function2 ��ȡÿҳÿ��Ŀ�ĵ�ַ��param1=ҳ��
def GetPageItems(Pagenum):
    pagesitem = URL+ str(Pagenum)
        
    req = urllib2.Request(pagesitem, headers=header)
    urlhtml = urllib2.urlopen(req)
    htmldata = urlhtml.read()  
    htmlpath = etree.HTML(htmldata)
    #ÿ���ĵ�ַƥ��,herf
    PageItemList = htmlpath.xpath('//tr[@class="tr3 t_one tac"]/td/a[@target="_blank"]/@href')
    
    #������������ÿ����ַ�ڲ��ı���
    browser.get(pagesitem)
    List = browser.find_elements_by_xpath("//h3/a[@target='_blank']")
    #Ϊ�˼�¼���ȣ�ÿʮ����ӡһ�ν��ȡ�
    RowNumber=0 
    for j in List:       
        for i in range(len(PageItemList)):
            if i == RowNumber:         
                PageItemurl="https://t66y.com/" + PageItemList[i]
                ImgPrifex="IMG_%03d%03d_" %(Pagenum,RowNumber)
                GetPagePictures(j.text,PageItemurl,ImgPrifex)
        RowNumber+=1
        if(RowNumber%10==0):
            print "the page %d have been load %d %%" %(Pagenum,RowNumber/10*10)
            

#Function3 ���ÿһ�����ӵ�ͼƬ��param1=ÿ���ı��⣬param2=ÿ�������ӵ�url,param3=ҳ��+���� 
def GetPagePictures(PageItemtitle,PageItemurl,ImgPrifex):
    
    #3_1 �������,�ؼ���ƥ��,ƥ�䲻��������
    PageItemtitle = re.sub('[?\s+\.\!\/_,$%^*(+\"\']+|[+��������������~@#��%����&*����]+-','-',PageItemtitle)
    if(head.IsMatch(PageItemtitle)==1):
        print 'PageItemtitle=',PageItemtitle.encode('gbk','ignore')  
    else:
        return

    #3_2 �жϴ���Ŀ���ļ����ǲ����Ѿ�����,����������,�������򴴽���
    #newfile=filetext2.strip().decode('utf-8')
    if not os.path.exists(os.path.join(SavePath,PageItemtitle)):
        os.makedirs(os.path.join(SavePath,PageItemtitle))
    else:
        return 
    #����Ŀ¼,�����ļ���    
    os.chdir(SavePath+PageItemtitle)
    
    #3_3 ����������������
    req = urllib2.Request(PageItemurl, headers=header)
    html = urllib2.urlopen(req)    
    htmldata = html.read()    
    htmlpath = etree.HTML(htmldata)
    ImageList = htmlpath.xpath('//input[@type="image"]/@src')
    for i in range(len(ImageList)):
        print "img=",ImageList[i]      
        ImgFileName=ImgPrifex+"%03d" %i
        SavePictures(ImageList[i],ImgFileName)

#Function4 ����ͼƬ
def SavePictures(ImgUrl,ImgName):  
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"
        , "Connection": "keep-alive"
        , "Referer": ImgUrl
    }    
    try:
        req = urllib2.Request(ImgUrl, headers=headers)
        urlhtml = urllib2.urlopen(req,timeout=20)
        respHtml = urlhtml.read()
        
        with open(ImgName+".jpg",'wb') as binfile:
            binfile.write(respHtml)
            time.sleep(0.1)       
    except:
        print         
           
GetPageAddr()                                      