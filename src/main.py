import scanPort
import hostScanning

target = input("请输入来选择功能：1=主机发现及操作系统识别，2=端口扫描及端口服务识别：")
if int(target) == 1:
    hostScanning.begin()
elif int(target) == 2:
    scanPort.begin()
else:
    print('输入有误，请重新输入')
#test5