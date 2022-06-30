# coding:utf-8
import requests
import random
from lxml import etree
import time
from ast import literal_eval


# User-Agent
user_agent = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36 Edg/101.0.1210.32",
]


# 作品分类url提取
def zpfl(url):
    try:
        header = {"User-Agent": random.choice(user_agent)}
        time.sleep(1)
        res = requests.get(url, headers=header, timeout=15)
        res.encoding = 'utf-8'
        data = etree.HTML(res.text)
        context = data.xpath('//div[@class="book-img-text"]/ul/li/div[@class="book-mid-info"]/h2/a/text()')
        conhref = data.xpath('//div[@class="book-img-text"]/ul/li/div[@class="book-mid-info"]/h2/a/@href')
        conimg = data.xpath('//div[@class="book-img-text"]/ul/li/div[@class="book-img-box"]/a/img/@src')
        name = []
        for i in range(len(context)):
            name.append([context[i], 'https:' + conhref[i], 'https:' + conimg[i]])
        return name
    except Exception as e:
        print(e)


# 作品目录页面
def info(url):
    try:
        header = {"User-Agent": random.choice(user_agent)}
        time.sleep(1)
        res = requests.get(url, headers=header, timeout=15)
        res.encoding = 'utf-8'
        data = etree.HTML(res.text)
        img = data.xpath('//*[@id="bookImg"]/img/@src')
        data_img = 'https:'+''.join(map(str, img)).split('\n')[0]  # img数据有换行
        name = data.xpath('//div[@class="book-info "]//em/text()')
        data_name = ''.join(name)
        author = data.xpath('//div[@class="book-info "]//span/a/text()')
        data_author = ''.join(author)
        tag = data.xpath('string(//p[@class="tag"])')  # 五个或者六个，第一个是作品状态，第四个是分类
        data_tag = tag.replace(' ', '').replace('\n\n\n\n', ' ').replace('\n\n', ' ').split(' ')
        info = data.xpath('//div[@class="book-intro"]/p/text()')  # 有换行，变成了列表，后期得处理数据
        data_info = '<br>'.join(info).replace(' ', '').replace('\n', '').replace(u'\u3000', '')
        name_catalog = data.xpath('//div[@class="volume"]/ul/li/h2/a/text()')    # 章节名 得加#Catalog显示
        href_catalog = data.xpath('//div[@class="volume"]/ul/li/h2/a/@href')    # 章节地址
        data_href_catalog = []
        for line in href_catalog:
            data_href_catalog.append('https:{}'.format(line))
        return {'img': data_img, 'name': data_name, 'author': data_author, 'tag': data_tag, 'info': data_info, 'name_catalog': name_catalog, 'href_catalog': data_href_catalog}
    except Exception as e:
        print(e)


# 章节页面
def read(url):
    try:
        header = {"User-Agent": random.choice(user_agent)}
        time.sleep(1)
        res = requests.get(url, headers=header, timeout=15)
        res.encoding = 'utf-8'
        data = etree.HTML(res.text)
        content = data.xpath('//div[@class="read-content j_readContent"]/p/span[@class="content-wrap"]/text()')

        return content
    except Exception as e:
        print(e)


def seek_url(name):
    url = 'https://www.qidian.com/soushu/%s.html'% (name)
    return url



url = 'https://www.qidian.com/free/'
info_url = 'https://book.qidian.com/info/1025908353/'
read_url = 'https://vipreader.qidian.com/chapter/1025908353/642509474/'
# print(read(read_url))    # 使用了ajax，占时无法解决

print(seek_url('斗破'))




