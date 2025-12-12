# tcp_chat_server.py
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from multiprocessing import Process
import os


def chat_with_client(conn, client_addr):
    """和单个客户端进行双向聊天"""
    print(f"[进程 {os.getpid()}] 开始和 {client_addr} 聊天～")
    try:
        while True:
            # 先接收客户端发来的消息
            data = conn.recv(1024)
            if not data:  # 客户端断开连接
                print(f"客户端 {client_addr} 已下线")
                break
            msg = data.decode("utf-8")
            if msg.strip().lower() == "exit":
                print(f"客户端 {client_addr} 主动退出")
                break
            print(f"[{client_addr}] 说: {msg}")

            # 再让服务端也能回复（这才是真正的双向！）
            reply = input(f"回复 {client_addr} >>> ").strip()
            if reply.lower() == "exit":
                conn.send(b"exit")
                break
            conn.send(reply.encode("utf-8"))

    except Exception as e:
        print(f"与 {client_addr} 通信异常: {e}")
    finally:
        conn.close()
        print(f"与 {client_addr} 的连接已关闭")


def main():
    server = socket(AF_INET, SOCK_STREAM)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 8080))
    server.listen(128)
    print("双向聊天服务器已启动，等待连接...")

    try:
        while True:
            conn, client_addr = server.accept()
            print(f"新朋友来了: {client_addr}")

            p = Process(target=chat_with_client, args=(conn, client_addr))
            p.daemon = True
            p.start()
            conn.close()  # 主进程关闭 conn，避免句柄泄露
    except KeyboardInterrupt:
        print("\n服务器已关闭")
    finally:
        server.close()


if __name__ == '__main__':
    main()