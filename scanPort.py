import socket
import sys

def scanPort():
    count = 0  # 发现端口的数量
    for port in range(int(port_start), int(port_end) + 1):
        sk = socket.socket()
        sk.settimeout(0.1)  # 等待端口响应时间
        conn_result = sk.connect_ex((host, port))  # 返回值，若为0则为端口开放
        if conn_result == 0:
            print('服务器{}的{}端口已开放'.format(host, port))
            count += 1
            print(sk.getsockname())
        sk.close()
    if count == 0:
        print(f'服务器{host}的{ports}端口均未开放')
        print("查询完毕")
    sys.exit()


host = input('请输入服务器ip地址:')
ports = input('请输入要扫描的端口范围，格式0-65536:')
port_start, port_end = ports.split('-')  # 以’-‘为分割符
h, o, s, t = host.split(".")
if not 65535 > int(port_end) > int(port_start) >= 0 or not 255 > int(h) > 0 or not 255 > int(o) > 0 or not 255 > int(s) > 0 or not 255 > int(t) > 0:
    print("ip地址有误，请重新输入")
    sys.exit()
scanPort()
