import ipaddress
import time
from subprocess import Popen, PIPE
import threading
import re
import sys

pattern = re.compile(r'TTL=[1-9][0-9]*')
threads = []  # 线程池
thread_max = threading.BoundedSemaphore(255)  # 最大信号量


# ping检测
def ping_check(ip):
    # ip = '127.0.0.1'
    check = Popen('ping {0}\n'.format(ip), stdin=PIPE, stdout=PIPE, shell=True)
    # 第一个参数为shell脚本执行ping ip的命令，同时必须将shell的参数设为True
    # stdin与stdout为输入输出命令同时用PIPE将一个函数结果直接导入另一个函数
    data = check.stdout.read()
    data = data.decode('GBK')  # 将前面传入的数据以gbk格式进行解码
    if 'TTL' in data or 'ttl' in data:  # 若data中包含ttl，证明主机存活，返回目标主机ip地址
        temp = re.search(pattern, data).group(0)
        ttl = temp.split('=')[1]
        print('The host {0} is up'.format(ip))
        if int(ttl) <= 32:
            print('对方系统是WIN95/98/ME')
        elif int(ttl) <= 64:
            print('对方系统是LINUX')
        elif int(ttl) <= 128:
            print('对方系统是WINNT/2K/XP')
        elif int(ttl) <= 256:
            print('对方系统是UNIX')


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


# 开始
def begin():
    host = input("Please input ip (示例：192.168.1.1): ")
    start = time.time()
    h, o, s, t = host.split('.')
    if not 255 >= int(h) >= 0 or not 255 >= int(o) >= 0 or not 255 >= int(s) >= 0 or not 255 >= int(t) >= 0:
        print("ip地址有误，请重新输入")
        sys.exit()
    host_number = 256 * 256 * 256 * int(h) + 256 * 256 * int(o) + 256 * int(s) + int(t)
    t = input("请输入你想沿当前ip往后查询多少个地址：")
    print('Start scanning......Please wait...')
    multi_threading_scanning(host_number, t)  # 取ip_add的除最后一个元素之外的值
    end = time.time()
    print("------------耗时{0:.5f}秒------------".format(end - start))


begin()
