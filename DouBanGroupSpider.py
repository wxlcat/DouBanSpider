from bs4 import BeautifulSoup
from gevent import monkey
import gevent
gevent.monkey.patch_socket()
gevent.monkey.patch_ssl()
import re
import time
import random
import Util
from Util import GetPageURL


class LoveGroupSpider():
    
    def __init__(self):
        self.SleepTimeMin = 0.1
        self.SleepTimeMax = 0.3
        self.PageBaseURL = 'https://www.douban.com/group/GuangZhoulove/discussion?start='
        self.PageDefaltURL = 'https://www.douban.com/group/GuangZhoulove/'
        self.HostURL = 'www.douban.com'
        self.StartStep = 25
        self.StartPage = 775
        self.PageNum = 1000
        self.PhotoPath = r'DoubanPhoto'
        self.PageFilePath = r'DouBanPage.txt'
        self.BlogFilePath = r'DouBanBlog.txt'
        # self.LogPath =r'DouBanLog.txt'
        
        self.re_pattern_bloglink = re.compile('^https://www.douban.com/group/topic/')
        self.re_pattern_blogimg = re.compile('doubanio.com/view/group_topic')

        self.filePage = open(self.PageFilePath, 'w')
        self.fileBlog = open(self.BlogFilePath, 'w')
        # self.fileLog = open(LogPath, 'w')
        
        self.cookies = {
        'bid':'tDtl1xwpa_o',
        '_pk_ref.100001.8cb4':'%5B%22%22%2C%22%22%2C1470197991%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D4em9oT6QEwWzZvCuwv_1Ujh9I8gj8AsUNeXqo_YOGFkR_IpetG_GDmXqRA9CAHzMByUEFe7RnzJYcO2zWXxgh_%26wd%3D%26eqid%3D973b3c38001e403e0000000657a17085%22%5D',
        '__utmt':'1', 
        '_pk_id.100001.8cb4':'88391a451737bd5c.1468899588.13.1470198152.1470194414.',
        '_pk_ses.100001.8cb4':'*', 
        '__utma':'30149280.632302979.1468899589.1470194201.1470197991.13',
        '__utmb':'30149280.16.5.1470198152273',
        '__utmc':'30149280',
        '__utmz':'30149280.1470197991.13.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic'
        }


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
        req = Util.RequestURLByGet(pageURL, headers, {})
        if not req is None:
            soup = BeautifulSoup(req.text, 'lxml')
            elements = soup.findAll(href=self.re_pattern_bloglink)
            coroutines = []
            for index, ele in enumerate(elements):
                blogLink = ele.get('href')
                blogTitle = ele.get('title')
                msg = '---------- SpiderBlogWeb:' + ('[%d/%d]' % (index+1,len(elements))) + '['+blogTitle+']'
                coroutines.append(gevent.spawn(self.SpiderBlogWeb,blogLink,pageURL,msg))
                #self.SpiderBlogWeb(blogLink, pageURL)
            gevent.joinall(coroutines)
            soup.decompose()
            
            if len(elements) <= 0:
                print '!!!!!!!!!! No blog link found !!!!!!!!!!'
                print req.text
            
            self.filePage.write(pageURL + '\n')
            self.filePage.flush()
        else:
            print '!!!!!!!!!! SpiderPageWeb Request is None !!!!!!!!!!'
            #print req.text
           
    def SpiderBlogWeb(self, blogURL, refererWeb, msg):
        headers = Util.GetHeaders(Host=self.HostURL, Referer=refererWeb)
        req = Util.RequestURLByGet(blogURL, headers, self.cookies)
        print msg
        if req:
            soup = BeautifulSoup(req.text, 'lxml')
            elements= soup.findAll(src=self.re_pattern_blogimg)
            threads = []
            for ele in elements:
                photoURL = ele.get('src')
#                 needDownload = Util.DownloadFile(photoURL), self.PhotoPath)
                threads.append(gevent.spawn(Util.DownloadFile, photoURL, self.PhotoPath, True))
#                 print str(needDownload),  photoURL
            gevent.joinall(threads)
            soup.decompose()
            self.fileBlog.write(blogURL + '\n')
#             if len(elements) > 0:
#                 print ''
        time.sleep(random.uniform(self.SleepTimeMin, self.SleepTimeMax))
    
    def GetPageURL(self, start):
        return self.PageBaseURL + str(start)
    
    def GetRefererURL(self, start):
        if start <= 0:
            return self.PageDefaltURL
        else:
            return GetPageURL(start -1)


