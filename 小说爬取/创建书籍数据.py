# coding:utf-8
import requests
import random
from lxml import etree
from ast import literal_eval
import os


# 个人的网站上传数据

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


'''
1. 拿到书名
2. 书名搜索拿到对应数据
 2.1 先去起点搜索，如果没有
 2.2 去三七中文网源地址文件拿到url，去读取对应的文件，如果没有拿到url
 2.3 去qijg拿到url
3. 数据提取
 3.1 书名、图片地址、连载状态、作者、简介等
 3.2 数据封装
 3.3 上传
'''

# 本地txt文件信息
def local_file():
    # 获取文件夹名字,避免爬取重复数据
    file_name_list = os.listdir('../xs')
    # 仅获取后缀为txt的文件名,为了方面后期处理删除文件后缀名
    file_name = [name.replace('.txt', '') for name in file_name_list if name[-4:] == '.txt']
    return file_name


# 三七中文本地url文件读取
def sanqi_url_txt():
    with open('777zw_book_url.txt', 'r', encoding='utf-8') as f:
        txt = f.read().replace("'", '').replace('{', '').replace('}', '').split(',')
        txt_dict = {}
        for line in txt:
            t = line.split(':')
            txt_dict[t[0].strip()] = txt_dict.get(t[1].strip()+':'+t[2].strip(), t[1].strip()+':'+t[2].strip())
        return txt_dict


# qbiqu文本地url文件读取
def qbiqu_url_txt():
    with open('book_url.txt', 'r', encoding='utf-8') as f:
        s = f.read()
        slist = literal_eval(s)
        txt_dict = {}
        for line in slist:
            txt_dict[line[0]] = line[1]
        return txt_dict


# 访问通用函数，utf-8
def get_url_utf8(url):
    try:
        header = {"User-Agent": random.choice(user_agent)}
        res = requests.get(url, headers=header, timeout=5)
        res.encoding = 'utf-8'
        data = etree.HTML(res.text)
        return {'data': data, 'mes': True}

    except Exception as e:
        return {'mes': False}


# 访问通用函数，gbk
def get_url_gbk(url):
    try:
        header = {"User-Agent": random.choice(user_agent)}
        res = requests.get(url, headers=header, timeout=5)
        res.encoding = 'gbk'
        data = etree.HTML(res.text)
        return {'data': data, 'mes': True}

    except Exception as e:
        return {'mes': False}


# 为下面的搜索做准备，都是本地url
qbiqu_url = qbiqu_url_txt()
sanqi_url = sanqi_url_txt()

# 起点搜素,是否有该书籍,有返回url
def qidian_sousu(name):
    try:
        print('起点搜索：' + name)
        url = 'https://www.qidian.com/soushu/%s.html' % name
        data = get_url_utf8(url)
        if data.get('mes'):
            info =  data.get('data').xpath('//*[@id="result-list"]/div/ul/li[1]/div[2]/h2/a/@title')
            data_info = ''.join(info)[:-4]
        if data_info == name:
            info_url = data.get('data').xpath('//*[@id="result-list"]/div/ul/li[1]/div[2]/h2/a/@href')
            data_info_url = 'https:'+''.join(info_url)
            return {'mes': True, 'url': data_info_url}
        else:
            return {'mes': False}
    except Exception as e:
        print(e)
        return {'mes': False}


# 三七搜索url，在本地url
def sanqi_sousuo(name):
    try:
        print('三七搜索：' + name)
        url = sanqi_url.get(name)
        if not url is None:
            return {'mes': True, 'url': url}
        else:
            return {'mes': False}
    except Exception as e:
        return {'mes': False}


# qbiqu搜索，本地url
def qbiqu_sousuo(name):
    try:
        print('qbiqu搜索：' + name)
        url = qbiqu_url.get(name)
        if not url is None:
            return {'mes': True, 'url': url}
        else:
            return {'mes': False}
    except Exception as e:
        return {'mes': False}


# 起点书籍信息页面
def qidian_info(url):
    try:
        if_data = get_url_utf8(url)
        if if_data.get('mes'):
            data = if_data.get('data')
            img = data.xpath('//*[@id="bookImg"]/img/@src')
            data_img = 'https:'+''.join(map(str, img)).split('\n')[0]  # img数据有换行
            name = ''.join(data.xpath('//div[@class="book-info "]//em/text()'))
            author = ''.join(data.xpath('//div[@class="book-info "]//span/a/text()'))
            category = data.xpath('string(//p[@class="tag"])')  # 五个或者六个，第一个是作品状态，第四个是分类
            data_category = category.replace(' ', '').replace('\n\n\n\n', ' ').replace('\n\n', ' ').split(' ')
            info = data.xpath('//div[@class="book-intro"]/p/text()')  # 有换行，变成了列表，后期得处理数据
            data_info = '<br>'.join(info).replace(' ', '').replace('\n', '').replace(u'\u3000', '')

        return {'mes': True, 'img': data_img, 'name': name, 'author': author, 'category': data_category, 'info': data_info}
    except Exception as e:
        print(e)
        return {'mes': False}


# 三七书籍信息页面
def sanqi_info(url):
    try:
        if_data = get_url_utf8(url)
        if if_data.get('mes'):
            data = if_data.get('data')
            img = ''.join(data.xpath('//div[@class="imgbox"]/img/@src'))
            name = ''.join(data.xpath('//div[@class="info"]/div/h1/text()'))
            author = data.xpath('//div[@class="info"]/div/div/p/text()')[0].split('者：')[1]
            content = ''.join(data.xpath('//div[@class="info"]/div[@class="desc xs-hidden"]/text()'))

        return {'mes': True, 'img': img, 'name': name, 'author': author, 'category': ['连载', '男生'], 'info': content}

    except Exception as e:
        print(e)
        return {'mes': False}


# qbiqu书籍信息页面
def qbiqu_info(url):
    try:
        if_data = get_url_gbk(url)
        if if_data.get('mes'):
            data = if_data.get('data')
            img = 'https://www.qbiqu.com' + ''.join(data.xpath('//div[@id="fmimg"]/img/@src'))
            name = ''.join(data.xpath('//div[@id="info"]/h1/text()'))
            author = data.xpath('//div[@id="info"]/p/text()')[0].split('者：')[1]
            content = ''.join(data.xpath('//div[@id="intro"]/p[1]/text()')).replace('\xa0', '').replace('\r', '').replace('\u3000', '')

        return {'mes': True, 'img': img, 'name': name, 'author': author, 'category': ['连载', '男生'], 'info': content}
    except Exception as e:
        print(e)
        return {'mes': False}


# 上传书籍数据封装处理
def book_data(info):
    # 书籍随机数据
    up = random.randint(100, 300)  # 顶
    down = random.randint(10, 260)  # 踩
    hits_day = random.randint(120, 400)     # 日人气
    hits_week = random.randint(300, 900)    # 周人气
    hits_month = random.randint(1200, 4000)   # 月人气 1200
    hits = random.randint(4000, 12000)   # 总人气
    rating = random.randint(1, 10)      # 总评分
    rating_count = random.randint(230, 800)   # 总评次
    recommend = random.randint(110, 960)     # 推荐票
    favorites = random.randint(210, 980)     # 收藏

    # 连载
    serialize_list = {'连载': 0, '完结': 1}
    fenlei = serialize_list.get(info.get('category')[0])

    # 分类
    category_list = {'男生': 4, '奇幻': 18, '玄幻': 18, '武侠': 19, '仙侠': 19, '历史': 20, '军事': 20,  '都市': 21, '科幻': 22, '悬疑': 23, '游戏': 34, '游戏竞技': 34,
            '其他': 35, '诸天无限': 42, '轻小说': 43, '体育': 44, '女生': 8, '古代言情': 25, '现代言情': 26, '浪漫青春': 27,
            '科幻空间': 37, '悬疑推理': 38, '同人衍生': 39, '现实生活': 40, '现实': 35, '短篇': 35}
    if len(info.get('category')) > 2:
        for data in info.get('category'):
            if len(data) == 4:
                if category_list.get(data[0:2]):
                    category = category_list.get(data[0:2])
                    break
                elif category_list.get(data[2:]):
                    category = category_list.get(data[2:])
                    break
            else:
                if category_list.get(data):
                    category = category_list.get(data)
                    break
                else:
                    category = 4
    else:
        category = 4

    # title：书名  category：分类  serialize：状态 author：作者 pic：封面地址 file：推荐 tag：标签 content：介绍

    return {'title':  info.get('name'), 'category': category, 'serialize': fenlei,
            'author':  info.get('author'), 'pic': info.get('img'), 'file': '', 'tag': '', 'content': info.get('info'),
            'up': up, 'down': down, 'hits_day': hits_day, 'hits_week': hits_week, 'hits_month': hits_month, 'hits': hits, 'rating': rating,
            'rating_count': rating_count, 'recommend': recommend, 'favorites': favorites, 'template_index': '', 'link': '', 'id': ''}


# 运行
def up_run(payload):
    try:
        url = 'http://xs.test.jiubanyipeng.com/admin/novel/add.html'
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0',
                   'Accept': 'application/json, text/javascript, */*; q=0.01',
                   'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                   'Accept-Encoding': 'gzip, deflate', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   'X-Requested-With': 'XMLHttpRequest', 'Content-Length': '', 'Origin': 'http://xs.jiubanyipeng.com',
                   'Connection': 'close', 'Referer': 'http://xs.jiubanyipeng.com/admin/novel/add.html'}

        cookies = {}

        r = requests.post(url, headers=headers, data=payload, cookies=cookies)
        return r.text
    except Exception as e:
        print(e)


# 遍历本地书籍名
for name in local_file():
    # 访问起点搜索是否还有该书籍，存在就返回url地址，反之就使用本地的
    qidian_get_sousuo = qidian_sousu(name)
    if qidian_get_sousuo.get('mes'):
        url = qidian_get_sousuo.get('url')
        book_info = qidian_info(url)
        if book_info.get('mes'):
            # 书籍信息的封装
            book_info_data = book_data(book_info)
            # 运行
            print(up_run(book_info_data))
            continue
        else:
            print('在访问书籍信息详细的时候失败了')
        continue

    sanqi_get_sousuo = sanqi_sousuo(name)
    print(sanqi_get_sousuo)
    if sanqi_get_sousuo.get('mes'):
        url = sanqi_get_sousuo.get('url')
        book_info = sanqi_info(url)
        if book_info.get('mes'):
            # 书籍信息的封装
            book_info_data = book_data(book_info)
            # 运行
            print(up_run(book_info_data))
            continue
        else:
            print('在访问书籍信息详细的时候失败了')
            continue

    qbiqu_get_sousuo = qbiqu_sousuo(name)
    if qbiqu_get_sousuo.get('mes'):
        url = qbiqu_get_sousuo.get('url')
        book_info = qbiqu_info(url)
        if book_info.get('mes'):
            # 书籍信息的封装
            book_info_data = book_data(book_info)
            # 运行
            print(up_run(book_info_data))
            continue
        else:
            print('在访问书籍信息详细的时候失败了')

    print("失败，不知道发生了什么")

