import socket


def main():
    # 1. 创建客户端 socket
    tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2. 服务器地址（改成你服务器的真实 IP）
    server_ip = "172.17.246.145"  # 如果在本机测试改成 "127.0.0.1"
    server_port = 8999
    server_addr = (server_ip, server_port)

    # 3. 连接服务器
    tcp_client_socket.connect(server_addr)
    print("连接成功！")

    # 4. 接收欢迎消息
    welcome_msg = tcp_client_socket.recv(1024).decode("utf-8")
    print(f"服务器说：{welcome_msg}")

    # 5. 循环聊天
    while True:
        send_data = input("请输入要发送的消息（输入 exit 退出）：")
        if send_data == "exit":
            print("您已退出聊天室")
            break
        if send_data.strip() == "":
            print("不能发送空消息")
            continue

        tcp_client_socket.send(send_data.encode("utf-8"))

    # 6. 关闭连接
    tcp_client_socket.close()


if __name__ == '__main__':
    main()