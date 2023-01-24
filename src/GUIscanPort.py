import socket
import sys
import threading
import time
from tkinter import *
from tkinter.messagebox import *

threads = []  # 线程池
thread_max = threading.BoundedSemaphore(65535)  # 最大信号量
# 发现端口的数量
count = 0


#  扫描端口模块
def scan_port(port, host, count=0):
    global portWorkText
    sk = socket.socket()
    sk.settimeout(0.5)  # 等待端口响应时间
    conn_result = sk.connect_ex((host, port))  # 尝试访问连接然后保存返回值，若为0则为端口开放
    if conn_result == 0:
        print('服务器{}的{}端口已开放'.format(host, port))
        system = sys.platform
        if 'w' in system:
            portWorkText += '服务器{}的{}端口已开放'.format(host, port)
        else:
            pass
        count += 1
        port_server(port)
        # print(sk.getsockname()) #显示套接字自己的地址
    sk.close()


#  多线程
def multi_threading_port(port, port_end, port_start, host):
    global portWorkText
    for i in range(int(port_end) - int(port_start)):
        thread_max.acquire()
        t = threading.Thread(target=scan_port, args=(port, host,))
        # 创建新线程执行scanPort，同时赋值ip=new_port
        threads.append(t)
        t.start()
        port = int(port) + 1
    for t in threads:
        t.join()

    text.insert(INSERT, portWorkText)
    root2.mainloop()


# 查询端口服务字典
def port_server(port_number):
    global portWorkText
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
            portWorkText += f'该端口的服务为{s}' + '\n'


# 开始
def portbegin():
    global root2
    global e1
    global e2
    host = e1.get()
    ports = e2.get()
    start = time.time()
    port_start, port_end = ports.split('-')  # 以’-‘为分割符
    h, o, s, t = host.split(".")
    if not 65535 >= int(port_end) > int(port_start) >= 0 or not 255 > int(h) > 0 or not 255 > int(
            o) > 0 or not 255 > int(s) > 0 or not 255 > int(t) > 0:
        showinfo(title='test', message='您输入的ip地址或端口数有误')
        sys.exit()
    multi_threading_port(port_start, port_end, port_start, host)
    print('端口服务为默认端口的情况，不排除自己改端口，所以服务显示有可能错误')
    end = time.time()
    print("------------耗时{0:.5f}秒------------".format(end - start))


# 能跑但是会爆一堆红字，不知道为啥，先写其他的去了


def gui():
    global root
    root.mainloop()


portWorkText = ''  # 装载结果最后输出
root = Tk()  # 生成主窗口
root.geometry('300x300')  # 改变窗体大小（‘宽x高’）
root.title('欢迎使用端口扫描功能')  # 窗口名字
root.geometry('+960+300')  # 改变窗体位置（‘+横坐标+纵坐标’）
root.resizable(True, True)  # 将窗口大小设置为可变/不可变
la0 = Label(root, text='ip地址').place(x=20, y=20)
la1 = Label(root, text='格式：1-65535').place(x=20, y=40)
img_gif = PhotoImage(file='img_gif.gif')
label_img = Label(root, image=img_gif).place(x=20, y=60)
# 第一个输入框位置功能
e1 = Entry(root)
e1.place(x=100, y=20)  # pack-包装 grid-网格 place-位置
e1.delete(0, END)  # 删除文本框里的值
e1.insert(0, '在这里输入ip地址...')
# 第二个输入框位置功能
e2 = Entry(root)
e2.place(x=100, y=40)
e2.delete(0, END)  # 删除文本框里的值
e2.insert(0, '在这里输入查询端口范围...')
# 两个按钮位置及功能
Button(root, text='ip查询起始', width=10, command=portbegin).place(x=10, y=250)
Button(root, text='点击退出', width=10, command=root.quit).place(x=200, y=250)
root2 = Tk()
root2.geometry('300x300')  # 改变窗体大小（‘宽x高’）
root2.title('hello')  # 窗口名字
root2.geometry('+1260+300')  # 改变窗体位置（‘+横坐标+纵坐标’）
root2.resizable(True, True)  # 将窗口大小设置为可变/不可变
scrollbar_v = Scrollbar(root2)
scrollbar_v.pack(side=RIGHT, fill=Y)
scrollbar_h = Scrollbar(root2, orient=HORIZONTAL)
text = Text(root2, width=50, height=30, undo=True, autoseparators=True)
text.pack()
root.mainloop()
