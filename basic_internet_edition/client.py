import socket

def main():
    s = socket.socket()
    host = '172.17.246.145' #你要链接的IP地址
    port = 12345
    s.connect((host,port)) #链接服务器
    msg = input("您要发送的信息是：")
    s.send(msg.encode("utf-8")) #发送信息
    print(s.recv(1024).decode("utf-8")) #接收信息
    s.close()

if __name__ == '__main__':
    main()