#-*- coding:utf-8 -*-
from LoveGroupSpider import LoveGroupSpider
import multiprocessing

spider = LoveGroupSpider()
spider.Run(1, 10)
