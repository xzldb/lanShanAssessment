import scanPort
import hostScanning
import webtitlescanning
import sshblast
import mysqlblast
import mssqlblast
import cmsscan
flag =True
while flag==True:
    target = input("请输入来选择功能：1=主机发现及操作系统识别，2=端口扫描及端口服务识别,3=webtitle探测,"+'\n'+
                   "4=ssh密码爆破，5=mysql密码爆破，6=mssql密码爆破，7=web识别cms：")
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
    else:
        print('输入有误，请重新输入')
    temp=input('是否继续进行扫描？若继续请输入y/yes/YES/Y：')
    if temp=='y'or 'yes'or "YES"or 'Y':
        flag=True
    else:
        flag=False
