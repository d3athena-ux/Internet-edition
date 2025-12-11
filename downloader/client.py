# tcp_file_client.py  ——  TCP 文件下载客户端
import socket


def main():
    # 1. 创建 TCP 客户端套接字
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2. 输入服务器地址和端口
    dest_ip = input("请输入服务器IP（比如 127.0.0.1）: ").strip()
    dest_port = int(input("请输入服务器端口（默认7788）: ").strip() or "7788")

    # 3. 连接服务器
    try:
        tcp_socket.connect((dest_ip, dest_port))
        print(f"成功连接到服务器 {dest_ip}:{dest_port}")
    except Exception as e:
        print("连接服务器失败:", e)
        return

    # 4. 输入要下载的文件名
    down_file_name = input("请输入要下载的文件名（带后缀，如 1.jpg）: ").strip()

    # 5. 把文件名发送给服务器
    tcp_socket.send(down_file_name.encode("utf-8"))

    # 6. 接收服务器发回的文件内容（最大接收 10MB，够用了）
    recv_data = tcp_socket.recv(1024 * 1024 * 10)  # 10MB缓冲

    # 7. 判断是否收到数据
    if recv_data:
        # 保存到本地，自动加上 new_ 前缀避免覆盖原文件
        save_name = "new_" + down_file_name
        with open(save_name, "wb") as f:
            f.write(recv_data)
        print(f"文件下载成功！已保存为: {save_name} （大小 {len(recv_data)} 字节）")
    else:
        print("下载失败：服务器上没有这个文件")

    # 8. 关闭连接
    tcp_socket.close()
    print("客户端已退出")


if __name__ == '__main__':
    main()