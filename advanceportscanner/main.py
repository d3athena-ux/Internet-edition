import socket
from optparse import OptionParser

# --------------------------------------
# 检查单个端口是否开放
# --------------------------------------
def check_port(ip, port):
    s = socket.socket()     # 创建一个 TCP socket
    s.settimeout(1)         # 设置 1 秒超时，避免连接不上卡住
    try:
        s.connect((ip, port))   # 尝试连接目标IP和端口
        s.close()
        return True            # 能连接说明端口开放
    except:
        return False           # 连接失败说明端口关闭或被过滤


# --------------------------------------
# 扫描一个端口列表，例如 [80, 21, 445]
# --------------------------------------
def scan(ip, portlist):
    for x in portlist:         # 对列表中的每个端口循环检查
        if check_port(ip, x):
            print(f"{ip}:{x} is open")   # 若开放
        else:
            print(f"{ip}:{x} is closed") # 若关闭


# --------------------------------------
# 扫描一个端口范围，例如 80~99
# --------------------------------------
def rscan(ip, s, e):
    for x in range(s, e + 1):      # range 不含最后一个，所以要 +1
        if check_port(ip, x):
            print(f"{ip}:{x} is open")
        else:
            print(f"{ip}:{x} is closed")


# --------------------------------------
# 主函数，用于解析命令行参数并调用对应扫描逻辑
# --------------------------------------
def main():
    # 使用说明
    usage = "usage: xxx.py -i ip地址 -p 端口"
    parse = OptionParser(usage=usage)

    # -i 或 --ip 后面跟目标 IP
    parse.add_option("-i", "--ip", type="string", dest="ipaddress",
                     help="your target ip here")

    # -p 或 --port 后面跟端口相关参数
    parse.add_option("-p", "--port", type="string", dest="port",
                     help="your target port here")

    # 解析命令行参数
    (options, args) = parse.parse_args()

    ip = options.ipaddress     # 读取输入的 IP
    port = options.port        # 读取输入的端口模式

    # 默认要扫描的几个常见服务端口
    defaultport = [135, 139, 445, 1433, 3306, 3389, 5944]

    # --------------------------------------
    # 多端口模式，例如：
    #   -p 80,21,445
    # --------------------------------------
    if ',' in port:
        port = port.split(',')     # 分割字符串 → ['80','21','445']
        a = []
        for x in port:
            a.append(int(x))       # 转成整数列表
        scan(ip, a)                # 调用列表扫描函数

    # --------------------------------------
    # 范围模式，例如：
    #   -p 80-99
    # --------------------------------------
    elif '-' in port:
        port = port.split('-')     # → ['80','99']
        s = int(port[0])           # 起始端口
        e = int(port[1])           # 结束端口
        rscan(ip, s, e)

    # --------------------------------------
    # 全端口扫描模式：
    #   -p all
    # 扫描 1 ~ 65535 所有端口
    # --------------------------------------
    elif 'all' in port:
        rscan(ip, 1, 65535)

    # --------------------------------------
    # 默认端口扫描模式：
    #   -p default
    # 扫描你预设的一组常见端口
    # --------------------------------------
    elif 'default' in port:
        scan(ip, defaultport)


# 屏蔽导入时执行，只在直接运行脚本时运行 main()
if __name__ == '__main__':
    main()
