import time
from subprocess import Popen, PIPE
import threading

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

    if 'TTL' in data:
        print('The host {0} is up'.format(ip))  # 将ip赋值进前面的括号内


# 多线程执行
def main(ip):
    # ip = '192.168.1.'
    for i in range(1, 255):
        new_ip = ip + str(i)
        thread_max.acquire()
        t = threading.Thread(target=ping_check, args=(new_ip,))
        # 创建新线程执行ping_check，同时赋值ip=new_ip
        threads.append(t)
        t.start()
    for t in threads:
        t.join()


ip = input("Please input ip (192.168.1.1): ")
print('Start scanning......Please wait...')
start = time.time()
main(ip[:-1])
end = time.time()
print("------------耗时{0:.5f}秒------------".format(end - start))
