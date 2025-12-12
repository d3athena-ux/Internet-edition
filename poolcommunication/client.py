# tcp_chat_client_fixed.py
from socket import socket, AF_INET, SOCK_STREAM

def main():
    client = socket(AF_INET, SOCK_STREAM)
    client.connect(('127.0.0.1', 8080))
    print("已连接到聊天服务器，输入 exit 退出，输入空行会被忽略")

    try:
        while True:
            msg = input("你说 >>> ").strip()
            if msg.lower() == "exit":
                client.send(b"exit")
                break
            if not msg:  # 客户端自己发空消息也忽略
                continue
            client.send(msg.encode("utf-8"))

            data = client.recv(1024)
            if not data:
                print("服务器已断开")
                break
            reply = data.decode("utf-8").strip()
            if reply.lower() == "exit":
                print("服务器让你下线了")
                break
            if not reply:  # 关键：收到空消息不退出，只忽略
                continue
            print(f"服务器说: {reply}")

    except Exception as e:
        print("连接异常:", e)
    finally:
        client.close()
        print("已退出")

if __name__ == '__main__':
    main()