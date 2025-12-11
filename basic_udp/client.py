# udp_client.py
import socket

def main():
    # 创建 UDP 套接字
    c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        # 用户输入要发送的内容
        text = input("--> ")

        # 如果输入 "exit" 就退出程序
        if text.strip().lower() == "exit":
            print("再见！")
            break

        # 发送数据到指定 IP 和端口（这里写死了服务端地址）
        # 改成你自己服务端的 IP，例如局域网 192.168.1.100
        c.sendto(text.encode("utf-8"), ("10.124.21.120", 6000))

        # 接收服务端回显的数据（最多 1024 字节）
        ans, _ = c.recvfrom(1024)

        # 只打印前 10 个字符（图片里是 ans[0]，应该是笔误，这里更合理）
        print("服务器回显:", ans[:10].decode("utf-8"))

    c.close()

if __name__ == '__main__':
    main()