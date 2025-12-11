# tcp_file_server.py  ——  TCP 文件下载服务端
import socket


def send_file(new_client_socket, client_addr):
    """
    处理单个客户端的文件下载请求
    :param new_client_socket: 已建立连接的客户端 socket
    :param client_addr: 客户端的 (ip, port) 元组
    """
    try:
        # 1. 接收客户端发送过来的“要下载的文件名”
        file_name = new_client_socket.recv(1024).decode("utf-8")
        print(f"客户端 {client_addr} 请求下载文件: {file_name}")

        # 2. 尝试打开并读取文件内容（用 rb 模式读取二进制）
        file_content = None
        try:
            with open(file_name, "rb") as f:
                file_content = f.read()
            print(f"文件 {file_name} 读取成功，大小 {len(file_content)} 字节")
        except FileNotFoundError:
            print(f"错误：服务端没有找到文件 {file_name}")
        except Exception as e:
            print(f"读取文件时发生未知错误: {e}")

        # 3. 把文件内容发回去（如果文件存在）
        if file_content:
            new_client_socket.send(file_content)
            print(f"已成功发送文件 {file_name} 给 {client_addr}")
        else:
            # 可选：告诉客户端“文件不存在”，这里发送一个空数据表示失败
            new_client_socket.send(b"")  # 发送空字节表示没有这个文件
            print(f"已通知客户端：文件 {file_name} 不存在")

    except Exception as e:
        print(f"与客户端 {client_addr} 通信出错: {e}")
    finally:
        # 无论如何都要关闭本次连接
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