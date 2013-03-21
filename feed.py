# -*- coding: utf-8 -*-
import os
import time
import urllib2
import urllib
import feedparser
import login

class rss:
    def __init__(self):
        self.feedFile = "feedlist"
        self.lastFile = "last"
        self.feedList = []
        self.lastList = []
        self.upContentList = []

    def __getFeedList(self):
        '''get the feed list from feedlist file'''
        with open(self.feedFile,'r') as f:
            content = f.readlines()
            for line in content:
                line = line.strip()
                if not line.startswith('#'):
                    self.feedList.append(line)

    def __getLastItem(self):
        '''get the last item from last file'''
        if not os.path.exists(self.lastFile):
            f=open(self.lastFile,'w')
            f.close()
        with open(self.lastFile,'r') as f:
            content = f.readlines()
            for line in content:
                line = line.strip()
                self.lastList.append(line)


    def run(self):
        self.__getFeedList()
        self.__getLastItem()
        for i,feed in enumerate(self.feedList):
            con = self.parse(feed,i)
            if con:
                self.upContentList.append(con)
        if len(self.upContentList):
            self.__updateLastFile()
            self.publish()

    def publish(self):
        '''publish on renren'''
        email = "815600970@qq.com"
        password = "13669134661"

        #email = "awesomethought@gmail.com"
        #password = "mryiting17"

        renrenSpider = login.spider(email,password)
        try:
            renrenSpider.login()
        except:
            print "login failed"

        print "Total :%d need to update"%(len(self.upContentList))

        for con in self.upContentList:
            #try:
            renrenSpider.share(con)
            #print con["summary"].encode("GB18030")
            #except:
            #    print "one share failed"
            time.sleep(20)

    def __updateLastFile(self):
        ''' update last file '''
        con = '\n'.join(self.lastList)
        with open(self.lastFile,'w') as f:
            f.write(con)

    def parse(self,feed,index):
        '''parse the feed'''
        r = feedparser.parse(feed)
        date = ""
        if "published" in r.feed:
            date =  r.feed.published
        else:
            date =  r.feed.updated
        needUpdate = False
        try:
            if date == self.lastList[index]:
                pass
            else:
                self.lastList[index] = date
                needUpdate = True
        except:
            self.lastList.append(date)
            needUpdate = True

        if needUpdate:
            img = self.__getImg(feed)
            return self.__getcontent(r,img)
        else:
            return
    def __getImg(self,feed):
        '''get the item img'''
        source = urllib2.urlopen(feed).readlines()
        for i,line in enumerate(source):
            if line.find("img")<>-1:
                tmpList = line.split()
                for cl in tmpList:
                    if cl.find("src")<>-1:
                        tmpListN = cl.split("=")
                        if len(tmpListN) >= 2:
                            link = tmpListN[-1]
                            link = link.strip("\"")
                            if link.startswith("http") and \
                                link.endswith("jpg"):
                                    return link
            if i>200:
                return ""
        return "" 


    def __getcontent(self,p_obj,img):
        '''get the conent of one feed'''
        con = {}
        con["img"] = img
        con["title"] = p_obj.entries[0].title
        con["link"] = p_obj.entries[0].link
        if "summary" in p_obj.entries[0]:
            con["summary"] = p_obj.entries[0].summary
        else:
            con["summary"] = p_obj.entries[0].description
        con["summary"] = con["summary"][:50]
        return con

if __name__ == "__main__":
    obj = rss()
    obj.run()

