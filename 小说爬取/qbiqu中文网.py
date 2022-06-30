import requests
import random
from lxml import etree
import time
from ast import literal_eval
import os

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


# qbiqu书籍列表
def book_url_1():
    try:
        url = 'https://www.qbiqu.com/paihangbang/'
        header = {"User-Agent": random.choice(user_agent)}
        res = requests.get(url, headers=header, timeout=15)
        res.encoding = 'gbk'
        data = etree.HTML(res.text)
        url_book = []
        for i in range(2, 7):  # 板块
            for j in range(2, 21):  # 板块列表
                context = data.xpath('//*[@id="main"]/div[%d]/ul[1]/li[%d]/a/text()' % (i, j))  # 书名
                conhref = data.xpath('//*[@id="main"]/div[%d]/ul[1]/li[%d]/a/@href' % (i, j))  # 书名地址
                context = ''.join(context)
                conhref = ''.join(conhref)
                url_book.append([context, conhref])
        with open('book_url.txt', 'a', encoding='utf-8') as f:
            f.write(url_book)
    except Exception as e:
        print(e)
        return False


# qbiqu书籍列表2
def book_url_2():
    try:
        url_book = []
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
        with open('book_url.txt', 'a', encoding='utf-8') as f:
            f.write(url_book)
    except Exception as e:
        print(e)
        return False


#  获取书籍列表以及书籍url地址数据
def read_txt():
    with open('book_url.txt', 'r', encoding='utf-8') as f:
        s = f.read()
        slist = literal_eval(s)
        return slist


# 获取章节以及章节url地址
def scrapyLink(url):
    try:
        header = {"User-Agent": random.choice(user_agent)}
        time.sleep(1)
        res = requests.get(url, headers=header, timeout=15)
        res.encoding = 'gbk'
        data = etree.HTML(res.text)
        context = data.xpath('//dl/dd/a/@href')
        conhref = data.xpath('//dl/dd/a/text()')
        name = []
        for i in range(len(context)):
            name.append([conhref[i], 'https://www.qbiqu.com' + context[i]])
        return name
    except Exception as e:
        print(e)


# 章节访问并写入文件
def web_url(txt_name, name, url):
    try:
        header = {"User-Agent": random.choice(user_agent)}
        time.sleep(0.5)
        res = requests.get(url, headers=header, timeout=15)
        res.encoding = 'gbk'
        data = etree.HTML(res.text)
        txt = data.xpath('//div[@id="content"]/text()')
        # 遍历文件名，特殊的去除掉
        name_book = txt_name.replace('/', ' ')
        with open('./%s.txt' % (name_book), 'a', encoding='utf-8') as f:
            f.write('####{}\n'.format(name))  # 写入章节，加#是为了自己之后的文章遍历
            for line in txt:
                if line != '\r\n':
                    lines = line.strip('\r\n').replace('\xa0', '')
                    f.write('{}\n'.format(lines))
        f.close()
        return True
    except Exception as e:
        print(e)
        return False


# 本地txt文件信息
def if_file():
    # 获取文件夹名字,避免爬取重复数据
    file_name_list = os.listdir('./')
    # 仅获取后缀为txt的文件名,为了方面后期处理删除文件后缀名
    file_name = [name.replace('.txt', '') for name in file_name_list if name[-4:] == '.txt']
    return file_name


# 判断文件是否存在
if os.path.exists('book_url.txt'):
    print("读取文件中...")
else:
    print("book_url.txt文件不存在，创建文件并爬取地址")
    book_url_1()
    book_url_2()

# 书籍数据
url_book = read_txt()
url_list = []

# 遍历书籍是否存在，第一次
for book_name, book_url in url_book:
    # 除去空格与特殊字符
    book_name = book_name.replace(' ', '').replace('/', ' ')
    if book_name in if_file():
        print('%s 书籍已经存在' % book_name)
    else:
        url_list.append([book_name, book_url])

# 章节运行定义
global sum_sum
sum_sum = 234  # 从第九个开始，之前的地址都是推荐章节

# 从第几本书籍开始
global sum
sum = 102  # 一共2547本书，从第1本到99本

sum_book = len(url_book)  # 运行总次数

while sum < len(url_book):
    txt_name = url_book[sum][0]  # 书籍名
    if txt_name in if_file():
        print('%s 书籍已经存在' % txt_name)
        sum += 1
        continue
    print("当前书名：", txt_name)
    print("当前书url地址：", url_book[sum][1])
    print("当前第{}，还剩余{}本".format(sum, sum_book - sum))
    txt_list = scrapyLink(url_book[sum][1])
    while sum_sum < len(txt_list):
        txt_pass = web_url(txt_name, txt_list[sum_sum][0], txt_list[sum_sum][1])
        if txt_pass:
            print('书名：{} {} 写入成功'.format(txt_name, txt_list[sum_sum][0]))
            sum_sum += 1
        else:
            print('ip被禁了，等待随机20秒到120秒后重新开始，当前第{}本书'.format(sum))
            time.sleep(random.randint(20, 120))
    sum += 1
    sum_sum = 9  # 重新定义章节
