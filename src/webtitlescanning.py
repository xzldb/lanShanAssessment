import re
import urllib.request

def begin():
    url = input("请输入探测的网址(需要包含http或https)：")
    response = urllib.request.urlopen(url)
    html = response.read()
    html = html.decode()
    tag = re.search(r'<title>(.*?)</title>', html).group(0)
    tag = tag[:-8]
    tag = tag[7:]
    print(tag)

def gettitletest():
    url = 'https://www.bilibili.com/'
    response = urllib.request.urlopen(url)
    html = response.read()
    html = html.decode()
    tag = re.search(r'<title>(.*?)</title>', html).group(0)
    tag = tag[:-8]
    tag = tag[7:]
    print(tag)