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
    sk.settimeout(0.5)  # 等待端口响应时间
    conn_result = sk.connect_ex((host, port))  # 尝试访问连接然后保存返回值，若为0则为端口开放
    if conn_result == 0:
        print('服务器{}的{}端口已开放'.format(host, port))
        count += 1
        port_server(port)
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


def port_server(port_number):
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
                print(f'该端口的服务为{s}')



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
print('端口服务为默认端口的情况，不排除自己改端口，所以服务有可能错误')
end = time.time()
print("------------耗时{0:.5f}秒------------".format(end - start))
# 能跑但是会爆一堆红字，不知道为啥，先写其他的去了
