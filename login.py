# -*- coding: utf-8 -*-
'''
======================================
此程序根据 http://www.oschina.net/code/snippet_148170_10661 内容改编
Adapted BY: bepcao
Mail:peterc9511@gmail.com
======================================
'''
from sgmllib import SGMLParser
import sys,urllib2,urllib,cookielib
import datetime
import time
class spider(SGMLParser):
    def __init__(self,email,password):
        SGMLParser.__init__(self)
        self.h3=False
        self.h3_is_ready=False
        self.div=False
        self.h3_and_div=False
        self.a=False
        self.depth=0
        self.names=""
        self.dic={}   
         
        self.email=email
        self.password=password
        self.domain='renren.com'
        try:
            cookie=cookielib.CookieJar()
            cookieProc=urllib2.HTTPCookieProcessor(cookie)
        except:
            raise
        else:
            opener=urllib2.build_opener(cookieProc)
            urllib2.install_opener(opener)       

    def login(self):
        print '开始登录'
        url='http://www.renren.com/PLogin.do'
        postdata={
                  'email':self.email,
                  'password':self.password,
                  'domain':self.domain  
                  }
        req=urllib2.Request(
                            url,
                            urllib.urlencode(postdata)            
                            )
        req.add_header('User-Agent','Mozilla/4.0 (compatible; MSIE 5.5; WindowsNT)') 
        self.file=urllib2.urlopen(req).readlines()
        for line in self.file:
            line = line.strip()
            if line.find("'id':")<>-1:
                tmp_list=line.split(":")
                self.id =tmp_list[-1].strip("',")
            elif line.find("get_check")<>-1:
                tmp_list=line.split(",",1)
                self.tok = tmp_list[0].split(":")[-1].strip("',")
                self.rtk = tmp_list[1].split(",",1)[0].split(":")[-1].strip("',")
            else:
                pass
        print self.id
        print self.tok
        print self.rtk
        #idPos = self.file.index("'id':'")
        #self.id=self.file[idPos+6:idPos+15]
        #tokPos=self.file.index("get_check:'")
        #self.tok=self.file[tokPos+11:tokPos+20]
        #rtkPos=self.file.index("get_check_x:'")
        #self.rtk=self.file[rtkPos+13:rtkPos+21]
        print "登陆成功"

    def publish(self,content):
        url1='http://shell.renren.com/'+self.id+'/status'
        postdata={
                  'content':content,
                  'hostid':self.id,
                  'requestToken':self.tok,
                  '_rtk':self.rtk,
                  'channel':'renren',
                  }
        req1=urllib2.Request(
                            url1,
                            urllib.urlencode(postdata)            
                            )
        self.file1=urllib2.urlopen(req1).read()
        print '%s:\n刚才使用你的人人账号 %s 发了一条状态\n内容为：(%s)'% (datetime.datetime.now(),self.email,postdata.get('content',''))

    def share(self,con):
        postdata = {
                    'comment':con["title"].encode("utf-8"),
                    'link:':con["link"],
                    'type':'6',
                    'url':con["link"],
                    'thumbUrl':con["img"],
                    'meta':'%22%22',
                    'nothumb':"off",
                    'title':con["title"].encode("utf-8"),
                    'summary':con["summary"].encode("utf-8"),
                    'hostid':self.id,
                    'requestToken':self.tok,
                    '_rtk':self.rtk,
                    'channel':'renren',}
        post_url = "http://shell.renren.com/" + self.id + "/share?1"
        req2 = urllib2.Request(post_url,urllib.urlencode(postdata))
        repon = urllib2.urlopen(req2)
        self.file2=repon.read()
        print self.file2.decode("utf-8")
        print "share success"

if __name__ == "__main__":
    email = "awesomethought@gmail.com"
    password = "mryiting17"

    renrenspider=spider(email,password)
    renrenspider.login()
    #content = "test"
    #renrenspider.publish(content)
    con ={ "link":"http://stackoverflow.com/questions/3470546/python-base64-data-decode","img":"","title":"Python base64 data decode - Stack Overflow","summary":"Stack Overflow  guys, I got a following peace of base64 encoded data, and I want to use python base64 module to extra..." }
    renrenspider.share(con)
