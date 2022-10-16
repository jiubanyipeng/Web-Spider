import requests
import time
import json
import os

CLIENT_ID = 'pPPmslzxxxxxxxxxxxxhKrpxHvXz'    # API Key
CLIENT_SECRET = 'VVbZElazxxxxxxxx5zj79VHG1hB'  # Secret Key
siteId = '000000'    # 你站点的id

home_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
stop_time = int(home_time.split(' ')[0].replace('-', '')) - 0     # 结束时间  减 0 是当天的时间，减 1 是昨天，减 2 是前天
start_time = stop_time - 2   # 开始时间  减2就是获取三天的数据

# 获取 code值 的地址，默认打印出来 不会进行访问
code_url = f'http://openapi.baidu.com/oauth/2.0/authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri=oob&scope=basic&display=popup'
print('请点击链接获取：',code_url)  # 请手动点击该链接，点击链接后进行登录，在登录成功的页面复制 code值，如果获取到了code_url则把它注释了
CODE = '215e190fa1ce17575f275a8db3e5cf98'  # 注意：以下的操作，当操作有误，code值就会改变，要重新填写新的code，值在上面这个链接获取

if len(CODE) < 15:
    print('CODE值有误，请重新填写')
    time.sleep(10)

global ACCESS_TOKEN, REFRESH_TOKEN      # ACCESS_TOKEN的有效期为一个月, REFRESH_TOKEN是当ACCESS_TOKEN过期用来重新刷新使用的，有效期十年


# 读取文件
def read_token():
    with open('baidu_token.txt', 'r') as f:
        return f.read()


# 写入文件
def write_token(data):
    with open('baidu_token.txt', 'w') as f:
        f.write(data)


# 获取 ACCESS_TOKEN
def get_access_token(CODE, CLIENT_ID, CLIENT_SECRET):
    try:
        access_url = f'http://openapi.baidu.com/oauth/2.0/token?grant_type=authorization_code&code={CODE}&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&redirect_uri=oob'
        access_data = requests.get(access_url)
        if access_data.status_code == 200:
            print('获取 ACCESS_TOKEN 成功，请重新运行')
            write_token(json.dumps(access_data.json()))
        elif access_data.status_code == 400:
            print('CODE值过期了，请重新获取填写', access_data.status_code)
    except Exception as e:
        print(e)


# 更新 ACCESS_TOKEN
def update_token(REFRESH_TOKEN, CLIENT_ID, CLIENT_SECRET):
    update_url = f'http://openapi.baidu.com/oauth/2.0/token?grant_type=refresh_token&refresh_token={REFRESH_TOKEN}&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}'
    update_data = requests.get(update_url)
    if update_data.status_code == 200:
        print('更新 ACCESS_TOKEN 成功，请重新运行')
        write_token(json.dumps(update_data.json()))
    else:
        print('更新 ACCESS_TOKEN 失败')


# 获取网站概况(趋势数据): 浏览量、访客数、IP数
def get_pv_uv_ip(access_token, siteId, start_time, stop_time):
    getapi_url = f'https://openapi.baidu.com/rest/2.0/tongji/report/getData?access_token={access_token}&site_id={siteId}&method=overview/getTimeTrendRpt&start_date={start_time}&end_date={stop_time}&metrics=pv_count,visitor_count,ip_count'
    getapi_data = requests.get(getapi_url)
    if getapi_data.status_code == 200:
        print('获取数据成功！')
        if getapi_data.json().get('error_msg'):
            print('Access token 过期了')
            update_token(REFRESH_TOKEN, CLIENT_ID, CLIENT_SECRET)
        return getapi_data.json()
    else:
        print('报错:未知原因，我暂时没遇到')
        return False


# 判断文件是否存在
if os.path.exists('baidu_token.txt'):
    try:
        token_data = json.loads(read_token())
        ACCESS_TOKEN = token_data.get('access_token')
        REFRESH_TOKEN = token_data.get('refresh_token')
    except Exception as e:
        print('报错:未知原因，我暂时没遇到')
        print(e)
else:
    get_access_token(CODE, CLIENT_ID, CLIENT_SECRET)


get_api = get_pv_uv_ip(ACCESS_TOKEN, siteId, start_time, stop_time)
if not get_api:
    print("没有获取到数据")
else:
    api_data = get_api.get('result')
    timeSpan = api_data.get('timeSpan')[0].split(' - ')
    items_time = api_data.get('items')[0]
    items_data = api_data.get('items')[1]
    for i in range(len(items_data)):
        print('从{}到{}的数据如下'.format(timeSpan[0], timeSpan[1]))
        print('日期：' + items_time[i][0])
        print('    浏览量PV：{} 访客数UV：{} IP 数：{}'.format(items_data[i][0], items_data[i][1], items_data[i][2]))

