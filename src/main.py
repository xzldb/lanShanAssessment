import sys

import hostScanning
import scanPort
import webtitlescanning
import sshblast
import mysqlblast
import mssqlblast
import cmsscan
def begin():
    flag =True
    while flag==True:
        target = input("请输入来选择功能：1=主机发现及操作系统识别，2=端口扫描及端口服务识别,3=webtitle探测,"+'\n'+
                       "4=ssh密码爆破，5=mysql密码爆破，6=mssql密码爆破，7=web识别cms,8=退出:")
        if int(target) == 1:
            hostScanning.begin()
        elif int(target) == 2:
            scanPort.begin()
        elif int(target) == 3:
            webtitlescanning.gettitle()
        elif int(target) == 4:
            sshblast.begin()
        elif int(target) == 5:
            mysqlblast.begin()
        elif int(target) == 6:
            mssqlblast.begin()
        elif int(target) == 7:
            cmsscan.begin()
        elif int(target) == 8:
            sys.exit()
        else:
            print('输入有误，请重新输入')
            begin()
        temp=input('是否继续进行扫描？若继续请输入y/yes/YES/Y：')
        if temp=='y'or 'yes'or "YES"or 'Y':
            flag=True
        else:
            sys.exit()
begin()