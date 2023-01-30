import re
import urllib.request
import time


def gettitle():
    url = input("请输入要查询的url：")
    print("--------开始进行webtitle扫描,这可能会花费一些时间,请耐心等待----------")
    timestart=time.time()
    response = urllib.request.urlopen(url)
    html = response.read()
    html = html.decode()
    tag = re.search(r'<title>(.*?)</title>', html).group(0)
    tag = tag[:-8]
    tag = tag[7:]
    print(tag)
    timeend=time.time()
    print("------------耗时{0:.5f}秒，cms功能完成------------".format(timeend - timestart))




def gettitletest():
    url = 'https://www.bilibili.com/'
    response = urllib.request.urlopen(url)
    html = response.read()
    html = html.decode()
    tag = re.search(r'<title>(.*?)</title>', html).group(0)
    tag = tag[:-8]
    tag = tag[7:]
    print(tag)

