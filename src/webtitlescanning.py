import re
import urllib.request
import hashlib


def gettitle():
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


with open('ip.txt', encoding='utf-8') as file_obj:
    url = file_obj.read()
    url = url.split('\n')
    num = len(url)
    for i in range(num):
        print(urllib.request.urlopen(url[i]).getcode())
        response = urllib.request.urlopen(url[i])
        html = response.read()
        data = html.decode()
        md5 = hashlib.md5()
        md5.update(data.encode('utf-8'))
        print("目标{}的网页Hash值:  {}".format(md5.hexdigest(), url[i]))
