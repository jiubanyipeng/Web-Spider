import requests
import random
from lxml import etree
import time
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


# 777zw 全部小说获取url
def quanbuxiaoshuo():
    url = 'https://www.777zw.net/xiaoshuodaquan/'
    header = {"User-Agent": random.choice(user_agent)}
    res = requests.get(url, headers=header, timeout=15)
    res.encoding = 'gbk'
    data = etree.HTML(res.text)
    book_name = data.xpath('//div[@id="main"]/div[@class="novellist"]/ul/li/a/text()')
    book_url_list = data.xpath('//div[@id="main"]/div[@class="novellist"]/ul/li/a/@href')
    url_dict = {}
    for s in range(len(book_name)):
        url_dict[book_name[s]] = 'https://www.777zw.net' + book_url_list[s]
    with open('777zw_book_url.txt', 'a', encoding='utf-8') as f:
        f.write(str(url_dict))


def re(url):
    try:
        header = {"User-Agent": random.choice(user_agent)}
        res = requests.get(url, headers=header, timeout=5)
        res.encoding = 'utf-8'
        data = etree.HTML(res.text)
        return {'data': data, 'mes': True}
    except Exception as e:
        return {'mes': False}

# 777zw 小说列表获取url
def xiaoshuo_list():
    url_dict = {}
    for i in range(1, 7):
        url = 'https://www.777zw.net/xiaoshuo%d/' % i
        header = {"User-Agent": random.choice(user_agent)}
        res = requests.get(url, headers=header, timeout=15)
        res.encoding = 'gbk'
        data = etree.HTML(res.text)
        sum = int(''.join(data.xpath('//*[@id="pagestats"]/text()')).split('/')[1])
        url_list = []
        for i in range(1, sum+1):
            url_list.append(url + '/index%d.html' % i)
        global sum_run
        sum_run = len(url_list)
        global run
        run = 0
        while run < sum_run:
            data = re(url_list[run])
            if data.get('mes'):
                book_name = data.get('data').xpath('//div[@class="newlistmulu"]/ul/li/a/text()')
                book_url = data.get('data').xpath('//div[@class="newlistmulu"]/ul/li/a/@href')
                for n in range(len(book_name)):
                    url_dict[book_name[n]] = 'https://www.777zw.net' + book_url[n]
                run += 1
            else:
                print('ip被禁了，等待随机10秒到20秒后重新开始')
                time.sleep(random.randint(10, 20))

    with open('777zw_book_url.txt', 'a', encoding='utf-8') as f:
        f.write(str(url_dict))


# url文件读取
def read_txt():
    with open('777zw_book_url.txt', 'r', encoding='utf-8') as f:
        txt = f.read().replace("'", '').replace('{', '').replace('}', '').split(',')
        txt_dict = {}
        for line in txt:
            t = line.split(':')
            txt_dict[t[0]] = txt_dict.get(t[1]+':'+t[2], t[1]+':'+t[2])
        return txt_dict


# 获取章节以及章节url地址
def section_url(url):
    try:
        data = re(url)
        context = data.get('data').xpath('//div[@class="section-box"]/ul/li/a/text()')
        conhref = data.get('data').xpath('//div[@class="section-box"]/ul/li/a/@href')
        name = []
        for i in range(len(context)):
            name.append([context[i], url + conhref[i]])
        return {'data': name, 'mes': True}
    except Exception as e:
        return {'mes': False}


# 章节访问并写入文件
def web_url(txt_name, name, url):
    try:
        data = re(url)
        txt = data.get('data').xpath('//div[@id="content"]/p/text()')
        with open('../xs3/%s.txt' % txt_name, 'a', encoding='utf-8') as f:
            f.write('####{}\n'.format(name))  # 写入章节，加#是为了自己之后的文章遍历
            s = ''
            sum = len(txt)
            for i in range(sum):
                if i == sum - 1:
                    continue
                s += txt[i] + '\n'
            f.write('{}\n'.format(s))

        return True
    except Exception as e:
        print(e)
        return False


# 判断文件是否存在
if os.path.exists('777zw_book_url.txt'):
    print("读取文件中...")
else:
    print("777zw_book_url.txt文件不存在，创建文件并爬取地址")
    quanbuxiaoshuo()
    xiaoshuo_list()

# 书籍数据
url_book = read_txt()
url_list = []  # 运行书籍列表


# 本地txt文件信息
def if_file():
    # 获取文件夹名字,避免爬取重复数据
    file_name_list = os.listdir('../xs3')
    # 仅获取后缀为txt的文件名,为了方面后期处理删除文件后缀名
    file_name = [name.replace('.txt', '') for name in file_name_list if name[-4:] == '.txt']
    return file_name

# 本地txt文件信息2
def if_file1():
    with open('book_names.txt', 'r', encoding='utf-8') as f:
        return f.read().split('\n')


def if_bookname(name):
    book_name = name.replace(' ', '').replace('/', ' ').replace('|', ' ').replace('<', ' ').replace('>', ' ').replace('\'', ' ').replace(':', ' ').replace('"', ' ').replace('*', ' ').replace('?', ' ').replace(';', ' ')
    return book_name


# 遍历书籍是否存在，第一次
for book_name, book_url in url_book.items():
    # 除去空格与特殊字符
    book_name = if_bookname(book_name)
    if book_name in if_file() or book_name in if_file1():
        print('%s 书籍已经存在' % book_name)
    else:
        url_list.append([book_name, book_url])


# 书籍运行次数
global sum
sum = 0   # 99

# 书籍运行总次数
sum_book = len(url_list)

# 章节运行次数
global sum_sum
sum_sum = 0

# 控制其他运行次数，如获取章节所有地址
global sum_sum_sum
sum_sum_sum = 0

while sum < sum_book:
    txt_name = url_list[sum][0]  # 书籍名
    # 第二次判断本地书籍是否存在
    if txt_name in if_file():
        print('%s 书籍已经存在' % txt_name)
        sum += 1
        continue

    print("当前书名：", txt_name)
    print("当前书url地址：", url_list[sum][1])

    txt_list = section_url(url_list[sum][1])
    if txt_list.get('mes'):
        txt_list_name = txt_list.get('data')
        txt_list_run = len(txt_list_name)
        print("当前第{}本，还剩余{}本，章节数:{}".format(sum, sum_book - sum, txt_list_run))
    else:
        print('获取章节失败，当前第{}次重新获取...'.format(sum_sum_sum + 1))
        time.sleep(random.randint(2, 5))
        sum_sum_sum += 1
        if sum_sum_sum == 3:
            print('%s已经获取三次，退出获取' % txt_name)
            sum_sum_sum = 0
            sum += 1
        continue

    if txt_list_run < 200:
        print('章节少于200章，退出')
        sum += 1
        continue
    while sum_sum < txt_list_run:
        txt_pass = web_url(txt_name, txt_list_name[sum_sum][0], txt_list_name[sum_sum][1])
        if txt_pass:
            print('书名：{} {} 写入成功'.format(txt_name, txt_list_name[sum_sum][0]))
            sum_sum += 1
        else:
            print('ip被禁了，等待随机20秒到120秒后重新开始，当前第{}本书'.format(sum))
            time.sleep(random.randint(20, 120))
    sum += 1
    sum_sum = 0  # 重新定义章节