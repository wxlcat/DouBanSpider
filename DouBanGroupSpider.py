from bs4 import BeautifulSoup
import re
import time
import random
import Util
from Util import GetPageURL


class LoveGroupSpider():
    
    def __init__(self):
        self.SleepTimeMin = 0.1
        self.SleepTimeMax = 1.0
        self.PageBaseURL = 'https://www.douban.com/group/GuangZhoulove/discussion?start='
        self.PageDefaltURL = 'https://www.douban.com/group/GuangZhoulove/'
        self.HostURL = 'www.douban.com'
        self.StartStep = 25
        self.StartPage = 219
        self.PageNum = 1923
        self.PhotoPath = r'd:\DoubanPhoto'
        self.PageFilePath = r'd:\DouBanPage.txt'
        self.BlogFilePath = r'd:\DouBanBlog.txt'
        # self.LogPath =r'd:\DouBanLog.txt'
        
        self.re_pattern_bloglink = re.compile('^https://www.douban.com/group/topic/')
        self.re_pattern_blogimg = re.compile('doubanio.com/view/group_topic')

        self.filePage = open(self.PageFilePath, 'w')
        self.fileBlog = open(self.BlogFilePath, 'w')
        # self.fileLog = open(LogPath, 'w')

    def Run(self):
        for i in range(self.StartPage, self.PageNum+1):
            start = (i -1) * self.StartStep
            print '==============','Spiding Page %d/%d' % (i,self.PageNum),'=============='
            self.SpiderPageWeb(start)
            
        self.filePage.close()
        self.fileBlog.close()
        # fileLog.close()
        
        print '============== Complete =============='
    
    
    def SpiderPageWeb(self, start):
        pageURL = self.GetPageURL(start)
        headers = Util.GetHeaders(Host=self.HostURL, Referer=self.GetRefererURL(start))
        req = Util.RequestURLByGet(pageURL, headers)
        if req:
            soup = BeautifulSoup(req.text, 'lxml')
            elements = soup.findAll(href=self.re_pattern_bloglink)
            for index, ele in enumerate(elements):
                blogLink = ele.get('href')
                blogTitle = ele.get('title')
                print '---------- SpiderBlogWeb:',  '[%d/%d]' % (index+1,len(elements)),  '['+blogTitle+']'
                self.SpiderBlogWeb(blogLink, pageURL)
            soup.decompose()
            
            if len(elements) <= 0:
                print '!!!!!!!!!! No blog link found !!!!!!!!!!'
                print req.text
            
            self.filePage.write(pageURL + '\n')
            self.filePage.flush()
           
    def SpiderBlogWeb(self, blogURL, refererWeb):
        headers = Util.GetHeaders(Host=self.HostURL, Referer=refererWeb)
        req = Util.RequestURLByGet(blogURL, headers)
        if req:
            soup = BeautifulSoup(req.text, 'lxml')
            elements= soup.findAll(src=self.re_pattern_blogimg)
            for ele in elements:
                photoURL = ele.get('src')
                noNeedDownload = Util.DownloadFile(photoURL, self.PhotoPath)
                print str(noNeedDownload),  photoURL
            
            soup.decompose()
            self.fileBlog.write(blogURL + '\n')
            if len(elements) > 0:
                print ''
        time.sleep(random.uniform(self.SleepTimeMin, self.SleepTimeMax))
    
    def GetPageURL(self, start):
        return self.PageBaseURL + str(start)
    
    def GetRefererURL(self, start):
        if start <= 0:
            return self.PageDefaltURL
        else:
            return GetPageURL(start -1)


