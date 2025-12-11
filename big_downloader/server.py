import socket
import os

def send_file(new_client_socket, client_addr):
    try:
        file_name = new_client_socket.recv(1024).decode("utf-8")
        print(f"客户端 {client_addr} 请求下载: {file_name}")

        try:
            file_size = os.path.getsize(file_name)
            with open(file_name, "rb") as f:
                content = f.read()
            print(f"正在发送文件，大小 {file_size / (1024*1024):.2f} MB")

            # 关键修改：先发8字节文件大小
            new_client_socket.send(file_size.to_bytes(8, 'big'))
            # 再发文件内容
            new_client_socket.sendall(content)
            print(f"发送完成 → {client_addr}")

        except FileNotFoundError:
            print(f"文件不存在: {file_name}")
            new_client_socket.send(b"\x00" * 8)  # 发送8个0表示文件不存在

    except Exception as e:
        print("发送出错:", e)
    finally:
        new_client_socket.close()

def main():
    # 1. 创建 TCP 服务端套接字
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 可选：让端口释放后立即可以重用（解决 “Address already in use” 错误）
    tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 2. 绑定地址（0.0.0.0 表示接受所有网卡的连接）
    tcp_server_socket.bind(("0.0.0.0", 7788))
    print("TCP 文件服务端启动成功，监听端口 7788...")

    # 3. 设置监听，最大等待连接数 128（原代码写10也行，128更常用）
    tcp_server_socket.listen(128)

    try:
        while True:
            # 4. 接受客户端连接
            new_client_socket, client_addr = tcp_server_socket.accept()
            print(f"新客户端连接: {client_addr}")

            # 5. 为每个客户端处理下载请求
            send_file(new_client_socket, client_addr)

    except KeyboardInterrupt:
        print("\n服务端已手动停止")
    finally:
        tcp_server_socket.close()


if __name__ == '__main__':
    main()