import socket


def main():
    # 1. 创建一个 TCP socket（套接字）
    s = socket.socket()  # 默认就是 TCP
    # 2. 获取本机的 IP 地址（通过解析一个知名域名）
    host = socket.gethostbyname(socket.gethostname())
    # 3. 常用端口 12345（自己随便挑一个 1024~65535 之间的）
    port = 12345

    # 4. 绑定本机 IP 和端口（告诉系统我要占用这个地址和端口）
    s.bind((host, port))

    # 5. 开始监听，等待客户端连接
    # 参数 5 表示：最多允许 5 个客户端排队等待连接
    s.listen(5)
    print(f"服务器已启动，监听在 {host}:{port}，等待客户端连接...")

    # 6. 接受客户端连接
    # accept() 会阻塞，直到有客户端连接进来
    # c: 用来和这个客户端通信的 socket
    # addr: 客户端的 IP 和端口号
    c, addr = s.accept()
    print(f"有客户端连接进来了！对方地址是：{addr}")

    # 7. 向客户端发送欢迎消息
    c.send("welcome".encode("utf-8"))  # 必须是 bytes 类型，所以要 encode

    # 8. 接收客户端发来的消息（最多接收 1024 字节）
    data = c.recv(1024).decode("utf-8")
    print(f"客户端说：{data}")

    # 9. 关闭与这个客户端的连接
    c.close()

    # 10. 关闭服务器 socket（如果不再接受新连接）
    s.close()


if __name__ == '__main__':
    main()