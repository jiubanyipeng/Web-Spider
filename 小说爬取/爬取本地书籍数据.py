import requests
import random
from lxml import etree
import time
from ast import literal_eval
import os

# 本地txt文件信息
def if_file():
    # 获取文件夹名字,避免爬取重复数据
    file_name_list = os.listdir('../xs2')
    # 仅获取后缀为txt的文件名,为了方面后期处理删除文件后缀名
    file_name = [name.replace('.txt', '') for name in file_name_list if name[-4:] == '.txt']
    return file_name


with open('book_names.txt', 'a', encoding='utf-8') as f:
    for i in if_file():
        f.write('{}\n'.format(i))


