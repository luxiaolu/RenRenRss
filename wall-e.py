# -*- coding: utf-8 -*-
'''
a class to get the feed update
'''
import sys
import os
import pickle
import time
import urllib2
import urllib
import feedparser
import renren


class rss:
    def __init__(self):
        if not os.path.exists("feedlist"):
            self.feedList={"default":[]}
            self.__dump()
        else:
            self.__load()

    def __dump(self):
        '''
        dump the feed list to disk
        '''
        f=open("feedlist",'w')
        pickle.dump(self.feedList,f)
        f.close()

    def __load(self):
        '''
        load the feed list from file 'feedlist'
        '''
        f=open("feedlist",'r')
        self.feedList = pickle.load(f)
        f.close()

    def update(self):
        email = "yourusername"
        password = "yourpassword"
        renrenspider=renren.renren(email,password)
        for key in self.feedList.keys():
            for i,oneFeed in enumerate(self.feedList[key]):
                feedUrl = oneFeed[0]
                feedLastUpdate = oneFeed[2]
                parseResult = feed(feedUrl,feedLastUpdate)
                parseResult.update()
                # get the new item's update time
                self.feedList[key][i][2]=parseResult.lastUpdate
                contentList = parseResult.updateCon
                for con in contentList:
                    renrenspider.shareLink(con)
                    print "wall-e: update one item from %s"%feedUrl
                    time.sleep(20)
        #self.__dump()

    def test(self,feedUrl):
        '''
        test if the feed could be colleted by wall-e
        '''
        try:
            parseResult = feed(feedUrl)
            parseResult.update()
            print "wall-e: test success"
            return True
        except:
            print "wall-e: test failed, can't parse this feed %s"%feedUrl
            return False

    def add(self,feedUrl,comment="",label="",isEnable="true"):
        if not self.test(feedUrl):
            print "wall-e: can't parse this new feed %s"%feedUrl
            return
        lastItemTime = ""
        if label:
            if label in self.feedList:
                self.feedList[label].append([feedUrl,comment,lastItemTime,isEnable])
            else:
                self.feedList[label]=[[feedUrl,comment,lastItemTime,isEnable]]
        else:
            self.feedList["default"].append([feedUrl,comment,lastItemTime,isEnable])
        self.__dump()

    def delByIndex(self,index,label):
        '''
        delete the feed by index
        '''
        if label in self.feedList:
            if len(self.feedList[label])>index:
                print "wall-e: the feed index is out of range, see 'wall-e list'"
            else:
                self.feedList[label].remove(self.feedList[label][index-1])
                self.__dump()
        else:
            print "wall-e: no such label %s, see 'wall-e list"%label
    
    def list(self):
        '''
        list all the feed
        '''
        for key in self.feedList.keys():
            print "Label: %s"%key
            for i,feed in enumerate(self.feedList[key]):
                print "    Index: %d\n        url: %s\n        lastItemTime: %s\n\
        comment: %s\n        enable: %s"%(i+1,feed[0],feed[2],feed[1],feed[3])

    def commentByIndex(self,index,label,comment=True):
        '''
        comment one feed
        '''
        if label in self.feedList:
            if len(self.feedList[label])>index:
                print "wall-e: the feed index is out of range, see 'wall-e list'"
            else:
                if comment:
                    self.feedList[label][index-1][3] = "false"
                else:
                    self.feedList[label][index-1][3] = "true"

                self.__dump()
        else:
            print "wall-e: no such label %s, see 'wall-e list"%label

class feed(object):
    '''
    a class to parse the feed using feedparser
    '''
    def __init__(self,feed,lastUpdate=""):
        self.feed = feed
        self.lastUpdate = lastUpdate
        self.result = feedparser.parse(feed)
        self.updateList=[]
        self.updateCon=[]

    def __getImg(self):
        '''
        get the item's img
        '''
        source = urllib2.urlopen(self.feed).readlines()
        for i,line in enumerate(source):
            if line.find("img")<>-1:
                tmpList = line.split()
                for cl in tmpList:
                    if cl.find("src")<>-1:
                        tmpListN = cl.split("=")
                        if len(tmpListN) >= 2:
                            link = tmpListN[-1]
                            link = link.strip("\"")
                            if link.startswith("http"):
                                if link.endswith("jpg") or \
                                link.endswith("png"):
                                    return link
            if i>200:
                return ""
        return ""
    def __getUpdateList(self):
        '''
        get the new publish item
        '''
        itemList = self.result.entries
        if not self.lastUpdate:
            self.updateList.append(itemList[0])
            return
        for i,item in enumerate(itemList):
            itemUpdate=""
            if item.published:
                itemUpdate = item.published
            else:
                itemUpdate = item.updated
            if i == 0:
                newUpdate = itemUpdate
            if itemUpdate == self.lastUpdate:
                self.lastUpdate = newUpdate
                return
            else:
                self.updateList.append(item)
        self.lastUpdate = newUpdate
        return
    
    def __getUpdateContent(self):
        '''
        get the item's content which need to update
        '''
        for item in self.updateList:
            con = {}
            con["img"] = self.__getImg()
            con["title"] = item.title
            con["link"] = item.link
            if "summary" in dir(item):
                con["summary"] = item.summary
            else:
                con["summary"] = item.description

            # for renren's length limit of content
            con["summary"] = con["summary"][:100]
            self.updateCon.append(con)

    def update(self):
        '''
        flow of update
        '''
        self.__getUpdateList()
        self.__getUpdateContent()

if __name__ == "__main__":
    rssObj = rss()

    argv = sys.argv
    # no argv
    if len(argv) == 1:
        rssObj.update()
    elif argv[1] == "test":
        if len(argv) == 2:
            print "wall-e: use 'test [url]' to test the new feed"
            sys.exit()
        rssObj.test(argv[2])
    elif argv[1] == "list":
        rssObj.list()
    elif argv[1] == "add":
        comment = ""
        label = ""
        try:
            feedUrl = argv[2]
            if len(argv) >= 4:
                comment = argv[3]
            if len(argv) == 5:
                label = argv[4]
        except:
            print "wall-e: use 'add [url[comment[label]]]' to add the new feed"
            sys.exit()
        rssObj.add(feedUrl,comment,label)
    elif argv[1] == "del":
        index = 0
        label = ''
        try:
            label = argv[2]
            index = int(argv[3])
        except:
            print "wall-e: use 'del [label[index]]' to delete one feed'"
            sys.exit()
        rssObj.delByIndex(index,label)
        
    elif argv[1] == "comment":
        index = 0
        label = ''
        try:
            label = argv[2]
            index = int(argv[3])
        except:
            print "wall-e: use 'comment [label[index]]' to comment one feed'"
            sys.exit()
        rssObj.commentByIndex(index,label)
    elif argv[1] == "update":
        rssObj.update()
    elif argv[1] == "help":
        print "wall-e: use 'test [url]' to test the new feed"
        print "        use 'list' to list all feeds"
        print "        use 'update' to update all the feeds"
        print "        use 'del [label[index]]' to delete one feed'"
        print "        use 'comment [label[index]]' to comment one feed'"
        print "        use 'add [url[comment[label]]]' to add the new feed"
        
    else:
        print "wall-e: %s is not a wall-f command, see 'wall-e help'"%argv[1]
