import os


# 本地txt文件信息
def if_file():
    # 获取文件夹名字,避免爬取重复数据
    file_name_list = os.listdir('../xs')
    # 仅获取后缀为txt的文件名,为了方面后期处理删除文件后缀名
    file_name = [name.replace('.txt', '') for name in file_name_list if name[-4:] == '.txt']
    return file_name


def if_file1():
    # 获取文件夹名字,避免爬取重复数据
    file_name_list = os.listdir('../xs_gx')
    # 仅获取后缀为txt的文件名,为了方面后期处理删除文件后缀名
    file_name = [name.replace('.txt', '') for name in file_name_list if name[-4:] == '.txt']
    return file_name


def if_file2():
    with open('重复书籍数据.txt', 'r', encoding='utf-8') as f:
        return f.read().split('\n')

global sum
global sum_sum
global ss_list
global name_list
name_list = []
sum = 0
ss_list = []
sum_sum = 0
'''
for i in if_file1():
    name = i
    with open('../xs_gx/%s.txt' % name, 'r', encoding='utf-8') as f:
        try:
            s = f.read().split('####')
            s_list = []
            for i in s:
                ss = i.split('\n')
                # 判断章节内容是否超过十行
                if ss[0] in '第' and len(ss) < 10:
                    sum_sum += 1
                # 章节重复
                if ss[0] not in s_list:
                    s_list.append(ss[0])
                else:
                    sum += 1
            if sum > 500:
                print('书名：{} ， 共有：{}章节， {}个章节重复'.format(name, len(s), sum))
                with open('重复书籍数据.txt', 'a', encoding='utf-8') as f:
                    f.write('{}\n'.format(name))


            # if sum_sum > 10:
                # print('书名：{}， 共有：{}章节， {}章节问题' .format(name,len(s),sum_sum))

            sum = 0
            sum_sum = 0
            ss_list = []
        except Exception as e:
            print('打开 %s 出错了。问题：%s'%(name,e))

'''
for book in if_file2():
    try:
        with open('../xs/%s.txt' % book, 'r', encoding='utf-8') as f:
            book_read = f.read().split('####')
            s_list = []
            for line in book_read:
                ss = line.split('\n')
                if ss[0] not in s_list:
                    if len(ss[0]) < 4 :
                        continue
                    s_list.append(ss[0])
                    with open('../xs_gx/%s.txt' % book, 'a', encoding='utf-8') as f:
                        f.write('####{}\n'.format(line))

    except Exception as e:
        print('打开 %s 出错了。问题：%s'%(book,e))
            

