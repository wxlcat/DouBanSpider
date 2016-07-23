from bs4 import BeautifulSoup
import requests
import re

URL = 'https://www.douban.com/group/GuangZhoulove/discussion?start=5225'

req = requests.get(URL)
# txt = req.content.decode('UTF-8', 'ignore')
soup = BeautifulSoup(req.content, 'lxml')
for item in soup.findAll(href = re.compile('^https://www.douban.com/group/topic')):
    print item
# print req.content
