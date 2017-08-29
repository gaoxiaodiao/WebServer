#!/usr/bin/python
#coding=utf-8
"""
*文件说明:扫描整合
*作者:高小调
*创建时间:2017年08月29日 星期四 14时20分8秒
*开发环境:Kali Linux/Python v2.7.13
"""
from modules import cdn_check
from modules import port_scan
import requests
from sys import argv
from lib import Spider
from modules import sql_check
from modules import webcms_check
from lib import Downloader
from modules import webshell_check
from modules import xss_check
from modules import bak_check
import socket
import urlparse
from bs4 import BeautifulSoup
import sys
import re   
import urllib2
reload(sys)
sys.setdefaultencoding('utf8')
def search(key,limit=20):
    page = 1
    re_dict = {}
    index = 1;
    while page*10 <= limit:
        if page == 1:
            search_url='http://www.baidu.com/s?wd=key&rsv_bp=0&rsv_spt=3&rsv_n=2&inputT=6391'
        else:
            search_url='http://www.baidu.com/s?wd=key&rsv_bp=0&rsv_spt=3&rsv_n=2&inputT=6391&pn='+str((page-1)*10)
        req=urllib2.urlopen(search_url.replace('key',key))   
        html=req.read()
        soup=BeautifulSoup(html,"html.parser")
        linkpattern=re.compile("href=\"(.+?)\"")
        div=soup.find('div',id='wrapper').find('div',id='wrapper_wrapper').find('div',id='container').find('div',id='content_left')
        re_dict={}
        start = 1
        end = 10
        if page > 1:
            start = (page-1)*10+1
            end = page*10
        for i in range(start,end):
            tmp1 = div.find('div',id=str(i))
            if(tmp1 is None):
                continue
            tmp2 = tmp1.find('h3')
            a = tmp2.find('a')
            re_link=linkpattern.findall(str(a))
            re_title=a.text
            try:
                r = requests.get(re_link[0],timeout=0.3)
                re_dict[re_title]=r.url
            except requests.exceptions.ConnectTimeout:
                print(str(index) + ".%s 请求超时"%re_title)
            except requests.exceptions.Timeout:
                print(str(index) + ".%s 打开超时"%re_title)
            except requests.exceptions.ConnectionError:
                print(str(index) + ".%s 连接失败"%re_title)
            except exceptions.Exception:
                print(str(index) + ".%s 其他异常"%re_title)
            print("%d-%s"%(i,re_title))
            index += 1
        page += 1
    return re_dict

def FullScan(url):
    #对url进行格式化
    url_info = urlparse.urlparse(url)
    scheme = url_info.scheme
    netloc = url_info.netloc
    path = url_info.path
    query = url_info.query
    if scheme == "":
        scheme = 'http'
    if netloc == "":
        print("网站地址不合法:域名为空!")
        return
    url = scheme + "://" + netloc
    #先进行CDN检测
    cdn_exist = cdn_check.run(url)
    cdn = "不存在CDN"
    if cdn_exist is True:
        #不存在CDN,则进行端口扫描
        ip = socket.gethostbyname(netloc)
        port_scan.PortScan(ip)
    else:
        cdn = "存在CDN"
    #爬虫抓取网站动态页面
    spider = Spider.Spider(url,10)
    dynamic_urls = spider.craw()
    sql="存在sql漏洞"
    xss="存在xss漏洞"
    sql_urls = []
    xss_urls = []
    for dynamic_url in dynamic_urls:
        if sql_check.run(dynamic_url) is True:
            sql_urls.append(dynamic_url)
        if xss_check.run(url) is True:
            xss_urls.append(dynamic_url)
    if sql_urls is None:
        sql = "无sql漏洞"
    if xss_urls is None:
        xss = "无xss漏洞"
    #CMS指纹识别
    cms_check = webcms_check.webcms(url,10)
    cms = cms_check.run()
    print("CDN:"+cdn)
    print("sql:"+sql)
    print("xss:"+xss)
    print("webcms:"+cms)
def SqlScan(url):
    #对url进行格式化
    url_info = urlparse.urlparse(url)
    scheme = url_info.scheme
    netloc = url_info.netloc
    path = url_info.path
    query = url_info.query
    if scheme == "":
        scheme = 'http'
    if netloc == "":
        print("网站地址不合法:域名为空!")
        return
    url = scheme + "://" + netloc + path
    #进行sql漏洞检测
    spider = Spider.Spider(url,10)
    dynamic_urls = spider.craw()
    sql_urls = []
    for dynamic_url in dynamic_urls:
        if sql_check.run(dynamic_url) is True:
            sql_urls.append(dynamic_url)
    if len(sql_urls)==0:
        return False,None
    else:
        return True,sql_urls
if __name__ == '__main__':
    #if argv[1] == "0":
    #    FullScan(str(argv[2]))
    #else:
    #    SqlScan(str(argv[2]))
    dict_url = search("inurl:asp?id=",100)
    for r in dict_url:
        print(dict_url[r])
        state,sql_urls=SqlScan(dict_url[r])
        if state == True:
            print(dict_url[r]+"存在sql漏洞")
            for url in sql_urls:
                print(url)
