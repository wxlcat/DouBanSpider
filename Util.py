import os
import random
import urllib
import urllib2
import requests
from _socket import error

Headers=[
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',  #chrome
        'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',                                           #IE
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.33 Safari/534.3 SE 2.X MetaSr 1.0',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E) QQBrowser/6.9.11079.201'          
        ]

def GetHeaders(**kwargs):
    headers={}
    headers['User-Agent'] = GetRandomUserAgent()
    headers.update(kwargs)
    return headers

def GetRandomUserAgent():
    index = random.randrange(0, len(Headers))
    return Headers[index]

# def GetBlogHeaders(refererWeb):
#     headers={}
#     headers['User-Agent'] = 'User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
#     headers['Host']= 'www.douban.com'
#     headers['Referer']= refererWeb
#     return headers

def GetPageURL(start):
    PageURL = 'https://www.douban.com/group/GuangZhoulove/discussion?start='
    return PageURL + str(start)

def GetFileNameByURL(url):
    index = url.rindex('/')    
    return url[index+1:]   

def GetFilePath(fileName, dirPath):
    if dirPath:
        return os.path.normcase(os.path.join(dirPath, fileName))
    else:
        return fileName
    
def DownloadFile(fileURL, dirPath):
    filePath = GetFilePath(GetFileNameByURL(fileURL), dirPath)
    noNeedDownload = os.path.exists(filePath)
    if not noNeedDownload:
        urllib.urlretrieve(fileURL, filePath)
    return noNeedDownload


def RequestURLByGet(url, headers):
    try:
        req = requests.request('get', url, headers=headers)
    except requests.exceptions.RequestException, e:
        print 'RequestException, ', e
    except urllib2.URLError, e:
        msg = 'URLError,'
        if hasattr(e, 'code'):
            msg = msg + ' Code: ' + e.code
        if hasattr(e, 'reason'):
            msg = msg + ' Reason: ' + e.reason
        print msg
    except Exception, e:
        print 'Exception, ', e
    except error, e:
        print 'Error, ', e
    else:
        return req
    
# def WriteLine(filePath, str):
#     file = open(filePath, 'w')
#     file.write(str)
#     file.flush()
#     file.close()
    
 
# def get_encoding(s):
#     if isinstance(s,unicode):
#         return "unicode"
#     try:
#         r = unicode(s)
#         return "ASCII"
#     except:
#         try:
#             r = s.decode("utf8")
#             return "utf8"
#         except:
#             try:
#                 r = s.decode("gbk")
#                 return "gbk"
#             except:
#                 try:
#                      r = s.decode("latin-1")
#                      return "latin-1"
#                 except:
#                     pass