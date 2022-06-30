# coding:utf-8
import requests
import ast
import csv

# 个人的网站，仅给出参考，我是自己在本地测试的，测试好直接上传都服务器
# 书名与id
def name_id_dict():
    with open("书名与id数据.csv") as f:
        reader = csv.reader(f)
        name_id_dict = {}
        rows = [row for row in reader]
        for i in range(1, len(rows)):
            name_id_dict[rows[i][1]] = rows[i][0]
    return name_id_dict


# 禁止上传书名id
def forbid_id():
    with open('禁止上传id数据.txt') as f:
        txt = f.read()
    return txt.split('\n')


# 写入禁止上传id
def forbid_id_write(info):
    with open('禁止上传id数据.txt', 'a', encoding='utf-8') as f:
        f.write('\n{}'.format(info))


# POST上传数据封装
def uploading_post(name, id):
    try:
        payload = {'split': 'custom', 'customsplit': '####', 'txtpath': '/uploads/txt/'+name+'.txt', 'novel_id': id, 'id': '', 'type': 'undefined'}
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0', 'Accept': '*/*',
                   'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                   'Accept-Encoding': 'gzip, deflate', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   'X-Requested-With': 'XMLHttpRequest', 'Content-Length': '', 'Origin': 'http://xs.test.jiubanyipeng.com',
                   'Connection': 'close', 'Referer': 'http://xs.test.jiubanyipeng.com/admin/novel/add.html'}
        cookies = {}
        url = 'http://xs.test.jiubanyipeng.com/admin/novel_chapter/import.html'
        r = requests.post(url, headers=headers, data=payload, cookies=cookies)
        r.encoding = 'utf-8'

        return ast.literal_eval(r.text)

    except Exception as s:
        return False


# 为了防止多次读写文件操作
book_forbid = forbid_id()
# 运行
for book, book_id in name_id_dict().items():
    if book_id in book_forbid:
        print(book_id + ': ' + book + '书籍信息存在')
        continue
    print('当前上传书名：' + book, 'ID:' + book_id)
    uploading_msg = uploading_post(book, book_id)
    if uploading_msg:
        print(uploading_msg)
        if uploading_msg.get('msg') == '章节导入成功！':
            forbid_id_write(book_id)
    else:
        print('上传失败')
        # 这里应该也写入失败名单的，我的就一万多数据就没有必要去搞了

'''
失败的
528
1837
'''




