
import requests
from bs4 import BeautifulSoup
import re
from urllib.request import urlretrieve as ur
import os
import sys

reg_imgur_file = re.compile('http[s]?://[i.]*imgur.com/\w+\.(?:jpg|png|gif)')#过滤器 正则表达

def downloadimg(articles):
    for article in articles: #遍历每页的标题和链接以及图片地址,下载图片在电脑上
        print(article.text,article['href'])
        if not os.path.isdir(os.path.join('download', article.text)):
            os.mkdir(os.path.join('download', article.text))
        res = requests.get('https://www.ptt.cc'+article['href'])
        images = reg_imgur_file.findall(res.text)
        print(images)
        for image in set(images):#保存图片
            ID = re.search('http[s]?://[i.]*imgur.com/(\w+\.(?:jpg|png|gif))',image).group(1)
            print(ID)#档案
            ur(image,os.path.join('download',article.text,ID))

def crawler(pages=3):
    if not os.path.isdir('download'):#检测是否有下载文件夹，如果没有就新建一个
        os.mkdir('download')
    url = 'https://www.ptt.cc/bbs/Beauty/index.html'

    for round in range(pages):
        res = requests.get(url) #抓取HTML
        soup = BeautifulSoup(res.text,'html.parser') #丢给BS
        tag_name = 'div.title a' #BS拿到标题链接
        articles = soup.select(tag_name)
        paging = soup.select('div.btn-group-paging a') #上一页链接
        next_url = 'https://www.ptt.cc'+paging[1]['href']
        url = next_url
        downloadimg(articles)

print(sys.argv)

crawler()

















