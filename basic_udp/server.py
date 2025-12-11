# udp_server.py
import socket

def main():
    # 创建 UDP 套接字（IPv4 + 数据报模式）
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 绑定本机端口 6000（"" 表示绑定所有网卡，如 0.0.0.0）
    s.bind(("", 6000))
    print("UDP 服务端已启动，监听端口 6000...")

    while True:
        # 接收最多 1024 字节的数据，同时返回 (数据, 对方地址)
        data, addr = s.recvfrom(1024)

        # 打印客户端信息
        print(f"connect by: {addr}")
        print("recv data :", data.decode("utf-8"))

        # 把收到的数据原样回给客户端（实现简单回显）
        s.sendto(data, addr)

    # 实际一般用 Ctrl+C 退出，不会走到这里
    s.close()

if __name__ == '__main__':
    main()