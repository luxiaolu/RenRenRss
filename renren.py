# -*- coding: utf-8 -*-
'''
the class with some actions on renren.com
'''
import sys,urllib2,urllib,cookielib
import datetime
import time
class renren(object):
    def __init__(self,email,password):
        self.email=email
        self.password=password
        self.domain='renren.com'

        self.id=''
        self.rtk=''
        self.tok=''
        try:
            cookie=cookielib.CookieJar()
            cookieProc=urllib2.HTTPCookieProcessor(cookie)
        except:
            raise
        else:
            opener=urllib2.build_opener(cookieProc)
            urllib2.install_opener(opener)       

        if not self.__login():
            raise

    def __login(self):
        print 'start login...'
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
        self.tok=self.rtk=self.id=""
        for line in self.file:
            line = line.strip()
            if line.find("'id':")<>-1:
                if self.id:
                    continue
                tmp_list=line.split(":")
                self.id =tmp_list[-1].strip("',")
            elif line.find("get_check")<>-1:
                if self.tok or self.rtk:
                    continue
                tmp_list=line.split(",",1)
                self.tok = tmp_list[0].split(":")[-1].strip("',")
                self.rtk = tmp_list[1].split(",",1)[0].split(":")[-1].strip("',")
            else:
                pass
        if self.tok and self.id and self.rtk:
            print "login success..."
            return "success"
        else:
            print "login failed"
            return None

    def status(self,content):
        '''
        public one status
        '''
        url='http://shell.renren.com/'+self.id+'/status'
        postdata={
                  'content':content,
                  'hostid':self.id,
                  'requestToken':self.tok,
                  '_rtk':self.rtk,
                  'channel':'renren',
                  }
        req=urllib2.Request(
                            url,
                            urllib.urlencode(postdata)            
                            )
        self.file1=urllib2.urlopen(req).read()
        print "-"*50
        print 'time: %s\naction: public status\nusername: %s'% (datetime.datetime.now(),self.email)
        print "-"*50

    def shareLink(self,con):
        '''
        share one link
        '''
        comment = "%s link:%s"%(con["title"],con["link"])
        postdata = {
                    'comment':comment.encode("utf-8"),
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
        self.file2=repon.read().decode("utf-8")
        if self.file2.find("ok") == -1:
            print "-"*50
            print 'time: %s\naction: share link\nusername: %s\n\
status: failed'% (datetime.datetime.now(),self.email)
            print "-"*50
        else:
            print "-"*50
            print 'time: %s\naction: share link\nusername: %s\n\
status: success'% (datetime.datetime.now(),self.email)
            print "-"*50

    def visit(self,peo_url):
        '''
        visit one's homepage
        '''
        urllib2.urlopen(peo_url).read()
        print "-"*50
        print 'time: %s\naction: visit user\nstatus\nusername: %s'% (datetime.datetime.now(),self.email)
        print "-"*50

if __name__ == "__main__":
    email = "yourusername"
    password = "yourpassword"

    renrenspider=renren(email,password)
    renrenspider.status("renren module test")
    con ={ "link":"http://stackoverflow.com/questions/3470546/python-base64-data-decode","img":"","title":"Python base64 data decode - Stack Overflow","summary":"Stack Overflow  guys, I got a following peace of base64 encoded data, and I want to use python base64 module to extra..." }
    renrenspider.shareLink(con)
    renrenspider.visit("http://www.renren.com/233653162")
