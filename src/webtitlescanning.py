import re
import urllib.request


def gettitle():
    url = input("请输入要查询的url：")
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
