import socket


def scanPort():
    host = input('请输入服务器ip地址:')
    ports = input('请输入要扫描的端口范围，格式0-65536:')
    port_start, port_end = ports.split('-')  # 以’-‘为分割符
    count = 0  # 发现端口的数量
    for port in range(int(port_start), int(port_end) + 1):
        print("正在查询端口" + str(port))
        sk = socket.socket()
        sk.settimeout(1)
        conn_result = sk.connect_ex((host, port))
        if conn_result == 0:
            print('服务器{}的{}端口已开放'.format(host, port))
            count += 1
        sk.close()
    if count == 0:
        print(f'服务器{host}的{ports}端口均未开放')


scanPort()
