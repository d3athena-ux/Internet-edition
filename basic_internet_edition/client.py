import socket   # Python 内置的网络编程模块

def main():
    # 1. 创建一个 TCP 客户端 socket（默认就是 TCP）
    s = socket.socket()                     # 或者写 socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 2. 服务器的 IP 地址（要连接的目标）
    # 注意：这里要改成你运行服务器的电脑的真实 IP！
    # 如果服务器和客户端在同一台电脑，可以用 '127.0.0.1'（本地回环地址）
    host = '127.0.0.1'        # ← 改成服务器的 IP，比如 '192.168.1.100'
    # 或者用 socket.gethostbyname(socket.gethostname()) 获取本机IP
    
    # 3. 服务器监听的端口（必须和服务器 bind 的端口完全一样）
    port = 12345
    
    # 4. 主动连接服务器
    # connect() 会尝试和服务器建立 TCP 三次握手
    # 如果服务器没开、端口不对、防火墙拦了，都会报错
    print(f"正在连接服务器 {host}:{port} ...")
    s.connect((host, port))                 # 连接服务器，阻塞直到成功或超时
    print("连接成功！可以开始聊天了～")
    
    # 5. 输入要发送给服务器的消息
    msg = input("您要发送的信息是：")         # 比如输入：你好，服务器！
    
    # 6. 发送消息给服务器
    # Python 字符串是 str 类型，网络传输必须是 bytes
    # 所以要用 .encode("utf-8") 转成字节
    s.send(msg.encode("utf-8"))
    print(f"已发送：{msg}")
    
    # 7. 接收服务器的回复
    # recv(1024) 表示最多接收 1024 字节
    # 返回的是 bytes 类型，用 decode("utf-8") 转回字符串
    # 也会阻塞，直到收到数据或对方关闭连接
    data = s.recv(1024).decode("utf-8")
    print(f"服务器回复：{data}")
    
    # 8. 关闭连接（礼貌地跟服务器说再见）
    s.close()
    print("连接已关闭，程序结束")

if __name__ == '__main__':
    main()
