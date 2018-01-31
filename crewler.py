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

#全局变量
URL="https://t66y.com/thread0806.php?fid=16&search=&page="
SavePath="E:\python\cl\mm\\"

#Function1 根据网页地址，获得每一页的地址,可扩展
def GetPageAddr():
    for Pagenum in range(1,101):
        GetPageItems(Pagenum)   

#Function2 获取每页每条目的地址。param1=页数
def GetPageItems(Pagenum):
    pagesitem = URL+ str(Pagenum)
        
    req = urllib2.Request(pagesitem, headers=header)
    urlhtml = urllib2.urlopen(req)
    htmldata = urlhtml.read()  
    htmlpath = etree.HTML(htmldata)
    #每条的地址匹配,herf
    PageItemList = htmlpath.xpath('//tr[@class="tr3 t_one tac"]/td/a[@target="_blank"]/@href')
    
    #调用浏览器获得每条地址内部的标题
    browser.get(pagesitem)
    List = browser.find_elements_by_xpath("//h3/a[@target='_blank']")
    #为了记录进度，每十条打印一次进度。
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
            

#Function3 获得每一条链接的图片。param1=每条的标题，param2=每条的链接的url,param3=页数+条数 
def GetPagePictures(PageItemtitle,PageItemurl,ImgPrifex):
    
    #3_1 标题规整,关键字匹配,匹配不到则跳过
    PageItemtitle = re.sub('[?\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+-','-',PageItemtitle)
    if(head.IsMatch(PageItemtitle)==1):
        print 'PageItemtitle=',PageItemtitle.encode('gbk','ignore')  
    else:
        return

    #3_2 判断此条目的文件夹是不是已经存在,存在则跳过,不存在则创建。
    #newfile=filetext2.strip().decode('utf-8')
    if not os.path.exists(os.path.join(SavePath,PageItemtitle)):
        os.makedirs(os.path.join(SavePath,PageItemtitle))
    else:
        return 
    #进入目录,创建文件。    
    os.chdir(SavePath+PageItemtitle)
    
    #3_3 断线重连保护机制
    req = urllib2.Request(PageItemurl, headers=header)
    html = urllib2.urlopen(req)    
    htmldata = html.read()    
    htmlpath = etree.HTML(htmldata)
    ImageList = htmlpath.xpath('//input[@type="image"]/@src')
    for i in range(len(ImageList)):
        print "img=",ImageList[i]      
        ImgFileName=ImgPrifex+"%03d" %i
        SavePictures(ImageList[i],ImgFileName)

#Function4 保存图片
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