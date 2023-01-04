import socket
import sys
import threading
import time

threads = []  # 线程池
thread_max = threading.BoundedSemaphore(65535)  # 最大信号量
# 发现端口的数量
count = 0

#  扫描端口模块
def scanPort(port, count=0):
    sk = socket.socket()
    sk.settimeout(0.1)  # 等待端口响应时间
    int(port)
    conn_result = sk.connect_ex((host, port))  # 尝试访问连接然后保存返回值，若为0则为端口开放
    if conn_result == 0:
        print('服务器{}的{}端口已开放'.format(host, port))
        count += 1
        # print(sk.getsockname()) #显示套接字自己的地址
    sk.close()

#  多线程
def main(port):
    for i in range(int(port_end) - int(port_start)):
        thread_max.acquire()
        t = threading.Thread(target=scanPort, args=(port,))
        # 创建新线程执行scanPort，同时赋值ip=new_port
        threads.append(t)
        t.start()
        port = int(port) + 1
    for t in threads:
        t.join()


host = input('请输入服务器ip地址:')
ports = input('请输入要扫描的端口范围，格式0-65535:')
start = time.time()
port_start, port_end = ports.split('-')  # 以’-‘为分割符
h, o, s, t = host.split(".")
if not 65535 >= int(port_end) > int(port_start) >= 0 or not 255 > int(h) > 0 or not 255 > int(o) > 0 or not 255 > int(
        s) > 0 or not 255 > int(t) > 0:
    print("ip地址有误，请重新输入")
    sys.exit()
main(port_start)
end = time.time()
print("------------耗时{0:.5f}秒------------".format(end - start))
# 能跑但是会爆一堆红字，不知道为啥，先写其他的去了
