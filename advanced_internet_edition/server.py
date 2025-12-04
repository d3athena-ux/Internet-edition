import socket


def main():
    # 1. 创建主 socket
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2. 绑定端口（"" 或 "0.0.0.0" 表示监听所有网卡）
    tcp_server_socket.bind(("", 8999))

    # 3. 设置监听（128 是等待队列最大长度）
    tcp_server_socket.listen(128)
    print("服务器已启动，监听 8999 端口，等待客户端连接...")

    # 4. 循环为多个客户端服务
    while True:
        # 5. 等待客户端连接（阻塞）
        new_client_socket, client_addr = tcp_server_socket.accept()
        print(f"客户端 {client_addr} 连接进来了！")

        # 6. 发送欢迎消息
        new_client_socket.send("欢迎来到聊天室！".encode("utf-8"))

        # 7. 循环为当前客户端服务多次（聊天）
        while True:
            try:
                recv_data = new_client_socket.recv(1024)
                if recv_data:  # 如果收到数据
                    print(f"客户端说：{recv_data.decode('utf-8')}")
                else:  # 收到空数据 = 客户端关闭了连接
                    print(f"客户端 {client_addr} 已下线")
                    break
            except:
                print(f"客户端 {client_addr} 异常断开")
                break

        # 8. 当前客户端结束服务，关闭连接
        new_client_socket.close()

    # 9. 主 socket 关闭（正常不会执行到这里，按 Ctrl+C 退出）
    tcp_server_socket.close()


if __name__ == '__main__':
    main()