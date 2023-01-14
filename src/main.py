import scanPort
import hostScanning
import webtitlescanning

target = input("请输入来选择功能：1=主机发现及操作系统识别，2=端口扫描及端口服务识别,3=webtitle探测：")
if int(target) == 1:
    hostScanning.begin()
elif int(target) == 2:
    scanPort.begin()
elif int(target) == 3:
    webtitlescanning.begin()
else:
    print('输入有误，请重新输入')
