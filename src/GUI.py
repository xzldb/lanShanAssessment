from tkinter import *
import tkinter.ttk
import scanPort
import hostScanning
import webtitlescanning
import sshblast
import mysqlblast
import mssqlblast
import cmsscan


root=Tk()
root.geometry('800x500')  # 改变窗体大小（‘宽x高’）
root.title('starlight的网络扫描器')  # 窗口名字
root.geometry('+500+300')  # 改变窗体位置（‘+横坐标+纵坐标’）
root.resizable(False, False)  # 将窗口大小设置为可变/不可变
latitle=Label(root,text='欢迎使用starlight的网络扫描器').place(x=320,y=20)
'''-----IP地址输入-------'''
labelip=Label(root,text='ip地址或网页url:').place(x=10,y=50)
ipEntry=Entry(root,width=20).place(x=110,y=50)
'''-----端口号输入-------'''
labelport=Label(root,text='端口号：').place(x=280,y=50)
portEntry=Entry(root,width=20).place(x=330,y=50)
'''-----扫描端口范围输入-------'''
labelportnumber=Label(root,text='端口范围(格式：xxx-xxx)：').place(x=490,y=50)
portnumberEntry=Entry(root,width=20).place(x=635,y=50)
'''-------操作功能选择-----------'''
studentClasses={'主机发现及操作系统识别','端口扫描及端口服务识别','webtitle探测','ssh密码爆破','mysql密码爆破','mssql密码爆破','web识别cms'}
comboPart=tkinter.ttk.Combobox(root, width=50, value=tuple(studentClasses))
labelpart=Label(root,text='功能选择:').place(x=10,y=80)
comboPart.place(x=80, y=80, width=150, height=20)
part=comboPart
if part=='主机发现及操作系统识别':
    hostScanning.begin()




root.mainloop()
