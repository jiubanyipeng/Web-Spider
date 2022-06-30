# -*- coding:UTF-8
import requests
import random
from lxml import etree
import time

# 设置requests库的重连接次数
requests.adapters.DEFAULT_RETRIES = 5


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


# 爬取的书板块 只要六个板块
url_lists = 'https://www.qbiqu.com/paihangbang/'
url_lists_s = 'https://www.qbiqu.com/wanben/'
# 书名以及地址
url_book = []
book = open('book_url.txt', 'w', encoding='utf-8')

# 书籍列表
def booke_url(url):
    try:
        header = {"User-Agent": random.choice(user_agent)}
        res = requests.get(url, headers=header, timeout=15)
        res.encoding = 'gbk'
        data = etree.HTML(res.text)
        for i in range(2, 7):  # 板块
            for j in range(2, 21):  # 板块列表
                context = data.xpath('//*[@id="main"]/div[%d]/ul[1]/li[%d]/a/text()' % (i, j))  # 书名
                conhref = data.xpath('//*[@id="main"]/div[%d]/ul[1]/li[%d]/a/@href' % (i, j))  # 书名地址
                context = ''.join(context)
                conhref = ''.join(conhref)
                url_book.append([context, conhref])
    except Exception as e:
        print(e)
        return False


# 书籍列表2
def bookes_url():
    try:
        for i in range(1, 83):
            url = 'https://www.qbiqu.com/wanben/1_%d' % (i)
            header = {"User-Agent": random.choice(user_agent)}
            time.sleep(1)
            res = requests.get(url, headers=header, timeout=15)
            res.encoding = 'gbk'
            data = etree.HTML(res.text)
            context = data.xpath('//div[@class="l"]/ul/li/span[@class="s2"]/a/text()')
            conhref = data.xpath('//div[@class="l"]/ul/li/span[@class="s2"]/a/@href')
            for s in range(len(context)):
                url_book.append([context[s], conhref[s]])
    except Exception as e:
        print(e)
        return False

booke_url(url_lists)
bookes_url()
print(url_book)
book.close()

# 获取章节地址
def scrapyLink(url):
    try:
        header = {"User-Agent": random.choice(user_agent)}
        res = requests.get(url, headers=header, timeout=15)
        res.encoding = 'gbk'
        data = etree.HTML(res.text)
        context = data.xpath('//dl/dd/a/@href')
        conhref = data.xpath('//dl/dd/a/text()')
        name = []
        for i in range(len(context)):
            name.append(['https://www.qbiqu.com' + context[i], conhref[i]])
        return name
    except Exception as e:
        print(e)
        return False

for line in range(len(url_book)):
    url_book_section = []
    txt_name = url_book[line][0]
    s_list = scrapyLink(url_book[line][1])
    with open('./%s.txt' % (txt_name), 'w', encoding='utf-8') as f:
        for i in range(9, len(s_list)):
            urls = s_list[i][0]  # 章节地址
            header = {"User-Agent": random.choice(user_agent)}
            res = requests.get(urls, headers=header, timeout=15)
            res.encoding = 'gbk'
            data = etree.HTML(res.text)
            time.sleep(random.randint(1, 5))  # 随机随机访问
            ss = data.xpath('//div[@id="content"]/text()')
            print(txt_name, s_list[i][1])
            # print(ss)
            f.write('####{}\n'.format(s_list[i][1]))
            for s in ss:
                if s != '\r\n':
                    aa = s.strip('\r\n').replace('\xa0', '')
                    f.write('{}\n'.format(aa))
    f.close()




