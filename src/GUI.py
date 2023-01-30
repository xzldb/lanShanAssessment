import socket
import ipaddress
import time
from subprocess import Popen, PIPE
import threading
import re
import sys
import urllib.request
import paramiko
import pymysql
import pymssql
import requests
import hashlib
from tkinter import *
import tkinter.ttk
from tkinter.messagebox import *


patternforwin = re.compile(r'TTL=[1-9][0-9]*')
patternforlinux = re.compile(r'ttl=[1-9][0-9]*')
threads = []  # 线程池
thread_max = threading.BoundedSemaphore(65535)  # 最大信号量
count = 0



'''---------------------------------------主机发现-----------------------------------------'''

def ping_check(ip):
    global worktext
    check = Popen('ping {0}\n'.format(ip), stdin=PIPE, stdout=PIPE, shell=True)
    # 第一个参数为shell脚本执行ping ip的命令，同时必须将shell的参数设为True
    # stdin与stdout为输入输出命令同时用PIPE将一个函数结果直接导入另一个函数
    data = check.stdout.read()
    data = data.decode('GBK')  # 将前面传入的数据以gbk格式进行解码
    if 'TTL' in data:  # 若data中包含ttl，证明主机存活，返回目标主机ip地址
        temp2 = re.search(patternforwin, data).group(0)
        ttl = temp2.split('=')[1]
        worktext += 'The host {0} is up'.format(ip)
        if int(ttl) <= 32:
            worktext += '对方系统是WIN95/98/ME' +'\n'
        elif int(ttl) <= 64:
            worktext += '对方系统是LINUX'+'\n'
        elif int(ttl) <= 128:
            worktext += '对方系统是WINNT/2K/XP'+'\n'
        elif int(ttl) <= 256:
            worktext += '对方系统是UNIX'+'\n'

# ping检测


# 多线程执行
def multi_threading_scanning(host_number, t):
    for i in range(1, int(t)):
        new_host_number = int(host_number) + i
        new_host = ipaddress.ip_network(new_host_number)  # 输出不为str类型的值，记得转换！！！
        new_host = str(new_host)
        new_host = new_host.split('/')[0]
        thread_max.acquire()
        t = threading.Thread(target=ping_check, args=(new_host,))
        # 创建新线程执行ping_check，同时赋值ip=new_ip
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    worktextprint()


# 开始
def hostScanningbegin():
    host=GUIhost
    temp=GUInumber
    start = time.time()
    h, o, s, t = host.split('.')
    if not 255 >= int(h) >= 0 or not 255 >= int(o) >= 0 or not 255 >= int(s) >= 0 or not 255 >= int(t) >= 0:
        print("ip地址有误，请重新输入")
        sys.exit()
    host_number = 256 * 256 * 256 * int(h) + 256 * 256 * int(o) + 256 * int(s) + int(t)
    print('Start scanning......Please wait...')
    multi_threading_scanning(host_number, temp)
    end = time.time()
    print("------------耗时{0:.5f}秒------------".format(end - start))


'''--------------------------------------端口扫描--------------------------------------------------'''


def scan_port(port, host, count=0):
    global worktext
    sk = socket.socket()
    sk.settimeout(0.5)  # 等待端口响应时间
    conn_result = sk.connect_ex((host, port))  # 尝试访问连接然后保存返回值，若为0则为端口开放
    if conn_result == 0:
        worktext+='服务器{}的{}端口已开放'.format(host, port)
        count += 1
        port_server(port)
        # print(sk.getsockname()) #显示套接字自己的地址
    sk.close()


#  多线程
def multi_threading_port(port, port_end, port_start, host):
    for i in range(int(port_end) - int(port_start)):
        thread_max.acquire()
        t = threading.Thread(target=scan_port, args=(port, host,))
        # 创建新线程执行scanPort，同时赋值ip=new_port
        threads.append(t)
        t.start()
        port = int(port) + 1
    for t in threads:
        t.join()
    worktextprint()


# 查询端口服务字典
def port_server(port_number):
    global worktext
    port_servers_dic = {21: 'FTP（File Transfer Protocol，文件传输协议）', 22: 'SSH（Secure Shell Protocol，安全外壳协议）',
                        23: 'Telnet（远程终端协议）	', 25: 'STMP（Simple Mail Transfer Protocol，简单邮件传输协议）',
                        53: 'DNS（Domain Name System，域名系统）',
                        80: 'HTTP（Hyper Text Transfer Protocol，超文本传输协议）或Apache/Tomcat/Nginx等中间件',
                        110: 'POP3（Post Office Protocol - Version 3，邮局协议版本3）	',
                        135: 'RPC（Remote Procedure Call，远程过程调用）',
                        139: 'SMB（Samba，用于文件、打印机、串口等的共享）	',
                        445: 'SMB（Samba，用于文件、打印机、串口等的共享）	',
                        443: 'HTTPS（Hyper Text Transfer Protocol over SecureSocket Layer，超文本传输安全协议）	',
                        1433: 'Microsoft SQL Server数据库	', 1521: 'Oracle数据库	', 3306: 'Mysql数据库	',
                        3389: 'RDP（Remote Desktop Protocol 远程桌面服务）	', 1099: 'RMI服务	', 1090: 'RMI服务	',
                        2181: 'Zookeeper服务	', 2375: 'Docker	', 5900: 'VNC', 5901: 'VNC	',
                        6379: 'Redis数据库	', 7001: 'WebLogic', 8080: 'Apache/Tomcat/Nginx等中间件	',
                        11211: 'Memcache服务	', 27017: 'MongoDB数据库	'}
    for p, s in port_servers_dic.items():
        if int(port_number) == p:
            worktext+=f'该端口的服务为{s}'+'\n'


# 开始
def scanPortbegin():
    global worktext
    host = GUIhost
    ports = GUIports
    start = time.time()
    port_start, port_end = ports.split('-')  # 以’-‘为分割符
    h, o, s, t = host.split(".")
    if not 65535 >= int(port_end) > int(port_start) >= 0 or not 255 > int(h) > 0 or not 255 > int(
            o) > 0 or not 255 > int(s) > 0 or not 255 > int(t) > 0:
        print("ip地址有误，请重新输入")
        sys.exit()
    worktext += '端口服务为默认端口的情况，不排除自己改端口，所以服务显示有可能错误'+'\n'
    multi_threading_port(port_start, port_end, port_start, host)

    end = time.time()
    print("------------耗时{0:.5f}秒------------".format(end - start))


'''-----------------------------webtitle扫描发现-----------------------------------------------'''


def webtitlebegin():
    global worktext
    url = GUIhost
    response = urllib.request.urlopen(url)
    html = response.read()
    html = html.decode()
    tag = re.search(r'<title>(.*?)</title>', html).group(0)
    tag = tag[:-8]
    tag = tag[7:]
    worktext+=tag
    worktextprint()

'''----------------------------------------------ssh爆破-------------------------------------------'''


def sshbrute(user, passw, host):
    global worktext
    global worksucesstext
    passw = str(passw)
    try:
        # 使用 paramiko.SSHClient 创建 ssh 对象
        ssh = paramiko.SSHClient()
        # 允许将信任的主机自动加入到host_allow 列表，此方法必须放在connect方法的前面，接受对方的公钥证书
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 登录 ssh，连接失败则抛出异常跳转到except并输出匹配错误的结果
        ssh.connect(hostname=host, port=22, username=user, password=passw, timeout=1)
        # 打印出成功登录的 用户名 和 密码
        print("login success! User:" + user, "Pass:" + passw)
        worksucesstext+="login success! User:" + user+"Pass:" + passw
    except:
        print("login failed!", "user:" + user, "pass:" + passw + '\n', end='')
        worktext +="login failed!"+ "user:" + user+ "pass:" + passw + '\n'

def multi_ssh(tempuser, temppasswd, target):  # 多线程
    userfile = tempuser.readlines()
    passwdfile = temppasswd.readlines()
    for a in userfile:
        for i in passwdfile:
            thread_max.acquire()
            t = threading.Thread(target=sshbrute, args=(a.replace('\n', ''), i.replace('\n', ''), target,))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
    worktextprint()
    worksucesstextprint()

def sshblastbegin():
    host = GUIhost
    tempuser = open('用户名.txt', 'r')
    temppasswd = open('密码库.txt', 'r')
    multi_ssh(tempuser, temppasswd, host)


'''---------------------------------------------mysql爆破------------------------------------'''


def mysqlblastbegin():
    host = GUIhost
    h, o, s, t = host.split('.')
    if not 255 >= int(h) >= 0 or not 255 >= int(o) >= 0 or not 255 >= int(s) >= 0 or not 255 >= int(t) >= 0:
        print("ip地址有误，请重新输入")
        sys.exit()
    port = GUIport
    tempuser = open('用户名.txt', 'r')
    temppasswd = open('密码库.txt', 'r')
    multi_mysql(tempuser, temppasswd, host, port)


def mysqlblast(user, passwd, host, port):
    global worktext
    global worksucesstext
    try:
        pymysql.connect(server=host, user=user, port=port, password=passwd, connect_timeout=1)
        worksucesstext+="mysql:{}:{}:{} {}".format(host, port, user, passwd)+'\n'
    except Exception:
        worktext+="mysql:{}:{} 用户名:{} 密码{}".format(host, port, user, passwd + '尝试连接失败')+'\n'
        pass


def multi_mysql(tempuser, temppasswd, host, port):
    userfile = tempuser.readlines()
    passwdfile = temppasswd.readlines()
    for u in userfile:
        for w in passwdfile:
            thread_max.acquire()
            t = threading.Thread(target=mysqlblast, args=(u.replace('\n', ''), w.replace('\n', ''), host, port,))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
    worktextprint()
    worksucesstextprint()


'''---------------------------------------------mssql爆破------------------------------------'''


def mssqlblatbegin():
    host = GUIhost
    h, o, s, t = host.split('.')
    if not 255 >= int(h) >= 0 or not 255 >= int(o) >= 0 or not 255 >= int(s) >= 0 or not 255 >= int(t) >= 0:
        print("ip地址有误，请重新输入")
        sys.exit()
    port = GUIport
    tempuser = open('用户名.txt', 'r')
    temppasswd = open('密码库.txt', 'r')
    multi_mssql(tempuser, temppasswd, host, port)


def mssqlblast(user, passwd, host, port):
    global worksucesstext
    global worktext
    try:
        pymssql.connect(server=host, user=user, port=port, password=passwd, connect_timeout=1)
        worksucesstext+="mssql:{}:{}:{} {}".format(host, port, user, passwd)+'\n'
    except Exception:
        worktext+="mssql:{}:{} 用户名:{} 密码{}".format(host, port, user, passwd + '尝试连接失败')+'\n'
        pass


def multi_mssql(tempuser, temppasswd, host, port):
    userfile = tempuser.readlines()
    passwdfile = temppasswd.readlines()
    for u in userfile:
        for w in passwdfile:
            thread_max.acquire()
            t = threading.Thread(target=mssqlblast, args=(u.replace('\n', ''), w.replace('\n', ''), host, port,))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
    worktextprint()
    worksucesstextprint()


'''------------------------------------------cms扫描识别-----------------------------------------------'''
'''------------------------指纹库内容------------------------'''
# 首页内容指纹库
body = {
    'content="WordPress': 'WordPress',
    'wp-includes': 'WordPress',
    'pma_password': 'phpMyAdmin',
    'hexo': 'hexo',
    'TUTUCMS': 'tutucms',
    'Powered by TUTUCMS': 'tutucms', 'Powered by 1024 CMS': '1024 CMS',
    'Discuz': 'Discuz',
    '1024 CMS (c)': '1024 CMS', 'Publish By JCms2010': '捷点 JCMS', }
# 请求头信息指纹库
head = {'X-Pingback': 'WordPress',
        'xmlrpc.php': 'WordPress', 'wordpress_test_cookie': 'WordPress', 'phpMyAdmin=': 'phpMyAdmin=',
        'adaptcms': 'adaptcms',
        'SS_MID&squarespace.net': 'squarespace建站',
        'X-Mas-Server': 'TRS MAS',
        'dr_ci_session': 'dayrui系列CMS',
        'http://www.cmseasy.cn/service_1.html': 'CmsEasy',
        'Osclass': 'Osclass',
        'clientlanguage': 'unknown cms rcms',
        'X-Powered-Cms: Twilight CMS': 'TwilightCMS',
        'IRe.CMS': 'irecms',
        'DotNetNukeAnonymous': 'DotNetNuke', }
# robots文件指纹库
robots = [
    'Tncms', '新为软件E-learning管理系统', '贷齐乐系统', '中企动力CMS', '全国烟草系统', 'Glassfish', 'phpvod', 'jieqi',
    '老Y文章管理系统',
    'DedeCMS']
# MD5指纹库
cms_rule = [
    '/images/admina/sitmap0.png|08cms|e0c4b6301b769d596d183fa9688b002a|',
    '/install/images/logo.gif|建站之星|ac85215d71732d34af35a8e69c8ba9a2|',
    '/jiaowu/hlp/Images/node.gif|qzdatasoft强智教务管理系统|70ee6179b7e3a5424b5ca22d9ea7d200|',
    '/theme/admin/images/upload.gif|sdcms|d5cd0c796cd7725beacb36ebd0596190|',
    '/themes/README.txt|drupal|5954fc62ae964539bb3586a1e4cb172a|',
    '/view/resource/skin/skin.txt|未知政府采购系统|61a9910d6156bb5b21009ba173da0919|',
    '/theme/admin/images/upload.gif|sdcms|d5cd0c796cd7725beacb36ebd0596190|',
    '/images/logout/topbg.jpg|TurboMail邮箱系统|f6d7a10b8fe70c449a77f424bc626680|', ]
# 特定网页指纹库
body_rule = [
    '/robots.txt|EmpireCMS|EmpireCMS|', '/images/css.css.lnk|KesionCMS(科讯)|kesioncms|',
    '/data/flashdata/default/cycle_image.xml|ecshop|ecshop|',
    '/admin/SouthidcEditor/Include/Editor.js|良精|southidc|', '/plugin/qqconnect/bind.html|PHP168(国徽)|php168|',
    '/SiteServer/Themes/Language/en.xml|SiteServer|siteserver|', '/system/images/fun.js|KingCMS|kingcms|',
    '/INSTALL.mysql.txt|Drupal(水滴)|drupal|', '/themes/default/style.css|ecshop|ECSHOP|',
    '/hack/gather/template/addrulesql.htm|qiboSoft(齐博)|qiboSoft|',
    '/phpcms/templates/default/wap/header.html|phpcms|phpcms']


def getweb(url):  # 尝试连接url中的网页并得到网页的请求头信息，网页的原始html，然后解码后成为中文的网页内容
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.114 Safari/537.36'}
    try:
        r = requests.get(url, timeout=5, headers=headers)
        encoding = requests.utils.get_encodings_from_content(r.text)[0]
        url_content = r.content.decode(encoding, 'replace')
        return str(r.headers), r.content, url_content
    except:
        pass


def cmsScan(url):
    global worktext
    # 首先通过robots文件来进行判定
    url_r = url + '/robots.txt'
    res = getweb(url_r)
    if res is not None:  # 如果robots文件存在，与robots进行匹配
        for robot in robots:
            if robot in res[2]:
                print('{}-->其CMS类型为:{}'.format(url, robot))
                worktext+='{}-->其CMS类型为:{}'.format(url, robot)+'\n'
    # 如果不存在，那就根据网页内容和请求头信息判定
    res = getweb(url)
    if res is not None:
        for k, v in head.items():
            if k in res[0]:
                print('{}其CMS类型为:{}'.format(url, v))
                worktext+='{}-->其CMS类型为:{}'.format(url, v)+'\n'
        for k, v in body.items():
            if k in res[2]:
                print('{}其CMS类型为:{}'.format(url, v))
                worktext+='{}-->其CMS类型为:{}'.format(url, v)+'\n'
        # 然后根据特定网址的内容判定
    for x in body_rule:
        cms_prefix = x.split('|', 3)[0]
        cms_name = x.split('|', 3)[1]
        cms_md5 = x.split('|', 3)[2]
        url_c = url + cms_prefix
        res = getweb(url_c)
        if res is not None:
            if cms_md5 in res[2]:
                print('{}其CMS类型为:{}'.format(url, cms_name))
                worktext+='{}-->其CMS类型为:{}'.format(url, cms_name)+'\n'
    # 最后根据MD5值判定
    for x in cms_rule:
        cms_prefix = x.split('|', 3)[0]
        cms_name = x.split('|', 3)[1]
        cms_md5 = x.split('|', 3)[2]
        url_s = url + cms_prefix
        res = getweb(url_s)
        if res is not None:
            md5 = hashlib.md5()
            md5.update(res[1])
            rmd5 = md5.hexdigest()
            if cms_md5 == rmd5:
                print('{}其CMS类型为:{}'.format(url, cms_name))
                worktext+='{}-->其CMS类型为:{}'.format(url, cms_name)+'\n'

            if res is None:
                print('{}暂时未搜索到其的cms地址'.format(url))
                worktext+='{}暂时未搜索到其的cms地址'.format(url)



def mulit_cms(tempip):
    ipfile = tempip.readlines()
    for url in ipfile:
        url = url.split('\n')[0]  # 去掉ip后面自带的回车键
        thread_max.acquire()
        t = threading.Thread(target=cmsScan, args=(url,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    worktextprint()


def cmsbegin():
    timestart = time.time()
    print("--------开始进行cms扫描,这可能会花费一些时间,请耐心等待----------")
    try:
        tempip = open('ip.txt', 'r')
        mulit_cms(tempip)
    except:
        print("请在源码文件目录下中的ip.txt目录中加入想要查找的ip地址")
    timeend = time.time()
    print("------------耗时{0:.5f}秒，主机发现功能正常------------".format(timeend - timestart))


'''-------------GUI函数定义----------------'''
GUIhost=''
GUIport=''
worktext=''
GUInumber=''
GUIports=''
worksucesstext=None
'''---------------窗口创建------------'''
root = Tk()
root.geometry('800x570')  # 改变窗体大小（‘宽x高’）
root.title('starlight的网络扫描器')  # 窗口名字
root.geometry('+500+300')  # 改变窗体位置（‘+横坐标+纵坐标’）
root.resizable(False, False)  # 将窗口大小设置为可变/不可变
latitle = Label(root, text='欢迎使用starlight的网络扫描器').place(x=320, y=20)
'''-----IP地址输入-------'''
labelip = Label(root, text='ip地址或网页url:').place(x=10, y=50)
ipEntry = Entry(root, width=20)
ipEntry.place(x=110, y=50)
'''-----端口号输入-------'''
labelport = Label(root, text='端口号：').place(x=280, y=50)
portEntry = Entry(root, width=20)
portEntry.place(x=330, y=50)
'''-----扫描端口范围输入-------'''
labelportnumber = Label(root, text='端口范围(格式：xxx-xxx)：').place(x=490, y=50)
portnumberEntry = Entry(root, width=20)
portnumberEntry.place(x=635, y=50)
'''-----查询数量输入-------'''
labelnumber=Label(root,text='查询数量:').place(x=260,y=80)
numberENtry=Entry(root,width=20)
numberENtry.place(x=330,y=80)
'''-------提示-------------'''
labeltips=Label(root,text='开始前请阅读下方注意事项!!!',fg='red').place(x=470,y=80)
labeltip1=Label(root,text='1.主机发现功能需要填入ip以及往后扫描的数量').place(x=10,y=450)
labeltip2=Label(root,text='2.端口扫描需要填入ip和扫描端口范围').place(x=10,y=470)
labeltip3=Label(root,text='3.webtitle探测和ssh密码爆破只需要输入目标url或者ip地址').place(x=10,y=490)
labeltip4=Label(root,text='4.mysql和mssql需要输入目标ip地址和准确端口号').place(x=10,y=510)
labeltip5=Label(root,text='5.cms识别在当前目录下的ip文件中输入url').place(x=10,y=530)
labeltip6=Label(root,text='6.密码爆破需要的时间较长，为了方便演示，密码文件设置的较为简陋，可自行添加').place(x=10,y=550)


'''-------操作功能选择-----------'''
studentClasses = {'主机发现及操作系统识别', '端口扫描及端口服务识别', 'webtitle探测', 'ssh密码爆破', 'mysql密码爆破',
                  'mssql密码爆破', 'web识别cms'}
comboPart = tkinter.ttk.Combobox(root, width=50, value=tuple(studentClasses))
labelpart = Label(root, text='功能选择:').place(x=10, y=80)
comboPart.place(x=80, y=80, width=150, height=30)


def getwork():
    global GUIhost
    global GUInumber
    global GUIports
    global GUIport
    GUIhost=ipEntry.get()
    GUInumber=numberENtry.get()
    GUIports=portnumberEntry.get()
    GUIport=portEntry.get()

def partchoose():
    global worktext
    part = comboPart.get()
    print(part)
    getwork()
    if part == '主机发现及操作系统识别':
        worktext=''
        hostScanningbegin()
    elif part =='端口扫描及端口服务识别':
        worktext = ''
        scanPortbegin()
    elif part == 'webtitle探测':
        worktext = ''
        webtitlebegin()
    elif part == 'ssh密码爆破':
        worktext = ''
        sshblastbegin()
    elif part == 'mysql密码爆破':
        worktext = ''
        mysqlblastbegin()
    elif part == 'mssql密码爆破':
        worktext = ''
        mssqlblatbegin()
    elif part == 'web识别cms':
        worktext = ''
        cmsbegin()
def clearText():
    workbox.delete('1.0','end')
choosebotton=Button(root,text='开始',width=20,command=partchoose).place(x=635,y=80)
clearbotton=Button(root,text='清屏',width=20,command=clearText).place(x=635,y=450)

def worktextprint():
    global worktext
    workbox.insert(INSERT,worktext)
def clearText():
    workbox.delete('1.0','end')

def worksucesstextprint():
    if worksucesstext != None:
        workbox.insert(INSERT,worksucesstext)
    else:
        workbox.insert(INSERT,'未得出结果，请尝试扩充密码库及用户库后再试~')

'''-------输出环境-----------'''
workbox=tkinter.Text(root,width=108)
workbox.place(x=20,y=120)
root.mainloop()
