#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-03-26 13:57:09
# @Author  : Lee @XiaMen
# @Version : 1.0
import os
import urllib,urllib2
import re

LOCAL_PATH=r"E:\delopy"
URL = r"http://openlinux.amlogic.com:8000/deploy/"

'''
	获取整个网页数据
'''
def getHtml(url):
	page = urllib.urlopen(url);
	html = page.read()
	return html

'''
	通过正则获取想要的资源列表
'''
def getResource(html):
    reg = r'</td><td><a href=\"(.+?)\">'
    resreg = re.compile(reg)
    reslist = re.findall(resreg,html)
    #print reslist
    return reslist

'''
回调函数
@a: 已经下载的数据块
@b: 数据块的大小
@c: 远程文件的大小
'''
def progresscbk(a, b, c):
	#print a , b , c
	if a*b >= c :
		print "100%,下载完成!"
		return 
	else:
		#per = 100. * a * b / c
		print '-'
		
def downloadResource(reslist):
	if not os.path.exists(LOCAL_PATH) :
		os.mkdir(LOCAL_PATH)
	for index in xrange(0,len(reslist)):
		if (reslist[index] != '') and (reslist[index] != '/'):
			local = os.path.join(LOCAL_PATH,reslist[index])
			remote = URL+reslist[index]
			print remote 
			if os.path.exists(local) and getLocalFileSize(local) != getRemoteFileSize(remote):
				print '重新下载!'
				urllib.urlretrieve(URL+reslist[index], local,progresscbk)
			else:
				print '未下载过，开始下载!'
				urllib.urlretrieve(URL+reslist[index], local,progresscbk)
				


def getLocalFileSize(path):
	os.path.getsize(path)


def getRemoteFileSize(url, proxy=None):
    """ 通过content-length头获取远程文件大小
        url - 目标文件URL
        proxy - 代理  """
    opener = urllib2.build_opener()
    if proxy:
        if url.lower().startswith('https://'):
            opener.add_handler(urllib2.ProxyHandler({'https' : proxy}))
        else:
            opener.add_handler(urllib2.ProxyHandler({'http' : proxy}))
    try:
        request = urllib2.Request(url)
        request.get_method = lambda: 'HEAD'
        response = opener.open(request)
        response.read()
    except Exception, e: # 远程文件不存在        
        return 0
    else:
        fileSize = dict(response.headers).get('content-length', 0)
        return int(fileSize)



if __name__ == '__main__':  
	html = getHtml(URL)
	res = getResource(html)
	downloadResource(res)

