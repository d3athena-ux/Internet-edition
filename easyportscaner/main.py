import sys
import socket

def check_port(ip, port):           # 改名避免冲突
    s = socket.socket()
    s.settimeout(1)                 # 关键！超时1秒，不卡
    try:
        s.connect((ip, port))
        s.close()
        return True
    except:
        return False                    # 不打印，交给调用者统一打印

def scan(ip, portlist):
    for x in portlist:
        if check_port(ip, x):
            print(f"{ip}:{x} is open")
        else:
            print(f"{ip}:{x} is closed")

def rscan(ip, s, e):
    for x in range(s, e + 1):       # +1 包含结束端口
        if check_port(ip, x):
            print(f"{ip}:{x} is open")
        else:
            print(f"{ip}:{x} is closed")

def main():
    defaultport = [21, 22, 23, 80, 135, 139, 445, 3306, 3389, 5944]

    if len(sys.argv) == 1:
        print("用法: python scanner.py [-help|-version] [ip] [ports]")
        sys.exit()

    arg = sys.argv[1]

    if arg == '-version':
        print('软件版本是1.0')
        sys.exit()
    elif arg == '-help':
        print('python scanner.py [ip] [port:80,99 或 80-99]')
        sys.exit()

    # 只有一个参数，且不是选项 → 默认扫描常见端口
    if len(sys.argv) == 2:
        scan(arg, defaultport)              # 这里是 IP
        return

    # 有三个参数：ip + 端口模式
    if len(sys.argv) == 3:
        ip = sys.argv[1]
        ports_arg = sys.argv[2]

        if ',' in ports_arg:                # 修复：用逗号判断
            port_str_list = ports_arg.split(',')
            port_list = [int(p) for p in port_str_list]
            scan(ip, port_list)

        elif '-' in ports_arg:              # 范围扫描
            start, end = ports_arg.split('-')
            rscan(ip, int(start), int(end))

if __name__ == '__main__':
    main()