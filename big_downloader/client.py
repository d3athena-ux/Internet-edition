# tcp_bigfile_client.py  —— 支持 1GB+ 大文件下载（带进度条）
import socket
import os


def download_big_file():
    # 1. 创建 socket 并连接服务器
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 输入服务器信息
    dest_ip = input("请输入服务器IP（例如 127.0.0.1）: ").strip()
    dest_port = int(input("请输入端口（默认7788）: ").strip() or "7788")

    try:
        tcp_socket.connect((dest_ip, dest_port))
        print(f"连接服务器成功 → {dest_ip}:{dest_port}")
    except Exception as e:
        print("连接失败：", e)
        return

    # 2. 输入要下载的文件名
    filename = input("请输入要下载的文件名（如 big_video.mp4）: ").strip()
    tcp_socket.send(filename.encode("utf-8"))

    # 3. 先接收文件大小（服务端要先发8字节表示文件总大小）
    #    注意：服务端必须配合修改！我们后面会给服务端也升级
    try:
        file_size_bytes = tcp_socket.recv(8)  # 先收8字节文件大小
        if len(file_size_bytes) < 8:
            print("服务器未返回文件大小，可能文件不存在")
            tcp_socket.close()
            return
        file_size = int.from_bytes(file_size_bytes, 'big')
        print(f"文件总大小: {file_size / (1024 * 1024):.2f} MB")
    except:
        print("接收文件大小失败，服务器可能未升级")
        tcp_socket.close()
        return

    # 4. 开始接收文件内容（分块接收 + 进度条）
    save_path = "[已下载]" + filename
    received_size = 0
    block_size = 1024 * 1024  # 每次接收 1MB

    with open(save_path, "wb") as f:
        print("开始下载，请稍等...")
        while received_size < file_size:
            # 动态调整最后一块的大小
            size = min(block_size, file_size - received_size)
            data = tcp_socket.recv(size)

            if not data:
                print("\n警告：连接中断，下载未完成！")
                break

            f.write(data)
            received_size += len(data)

            # 超简单的进度条
            progress = received_size / file_size * 100
            bar_length = int(progress // 2)
            bar = "█" * bar_length + "░" * (50 - bar_length)
            print(
                f"\r下载进度: |{bar}| {progress:.2f}%  ({received_size // (1024 * 1024)}MB/{file_size // (1024 * 1024)}MB)",
                end="")

    print("\n\n下载完成！")
    print(f"文件已保存为: {os.path.abspath(save_path)}")
    tcp_socket.close()


if __name__ == '__main__':
    download_big_file()