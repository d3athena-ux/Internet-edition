import socket


def main():
    # 【BUG1】拼写错误！AF_INRT 应该是 AF_INET
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # ← 改这里！！！

    host = '172.17.246.145'  # 受害者（即 server）的 IP
    port = 12345

    # 【BUG2】如果 server 没开，这里会直接抛异常崩溃
    try:
        s.connect((host, port))
    except Exception as e:
        print("连接失败！请确认 server 已启动，IP 端口是否正确")
        print(e)
        return  # ← 加个 return 直接退出

    print("连接成功！")

    while True:
        # 接收 server 发来的数据（欢迎语、命令执行结果等）
        data_recv = s.recv(1024)  # 这里还是 bytes
        if not data_recv:  # 【BUG3】server 意外断开时会收到 b''，必须判断！
            print("服务器已断开连接")
            break

        print(data_recv.decode("utf-8", errors="ignore"), end="")  # end="" 防止多空行

        # 只有当 server 给我们提示的时候我们才输入（防止刚连上就卡着要你输入）
        # 但你现在的逻辑是每次收到数据就立刻让你输入，这样其实是对的，只是体验差一点
        # 先保留你的原始逻辑，稍后你再优化也行

        msg = input("请输入命令")  # 这里不写提示词，纯等待用户敲命令
        if msg.strip() == "":  # 防止不小心按回车就发空字符串
            continue

        # 【BUG4】如果用户输入 exit 后我们自己也得退出，不然还会继续循环
        # 其实可以不退出，继续连下一个也行，但大多数人期望 exit 就彻底结束
        if msg.strip().lower() == "exit" and "cmd" in str(data_recv):  # 粗暴判断已经在 cmd 模式
            s.send(msg.encode("utf-8"))
            print("已退出远程 cmd，再见！")
            break  # ← 可选：exit 后彻底结束程序

        s.send(msg.encode("utf-8") + b"\n")  # 建议加个换行，server 端好判断命令结束

    s.close()
    print("客户端已关闭")


if __name__ == '__main__':
    main()