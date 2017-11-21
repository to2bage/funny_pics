"""
可以建立连接了
"""
import select
import socket
import queue

def main():
    proxy_sock = socket.socket()
    proxy_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    proxy_sock.setblocking(False)
    proxy_addr = ("0.0.0.0", 9999)
    proxy_sock.bind(proxy_addr)
    proxy_sock.listen(5)
    print("Prox Server is listening...")

    rli = [proxy_sock]
    wli = []
    sock_to_queue = {}

    while True:
        readable, writeable, excepable = select.select(rli, wli, rli)
        for item in readable:
            if item is proxy_sock:
                # 处理新连接
                client_sock, client_addr = item.accept()
                print("Welecom %s:%s" % (str(client_addr[0]), str(client_addr[1])))
                client_sock.setblocking(False)
                rli.append(client_sock)
                sock_to_queue[client_sock] = queue.Queue()
            else:
                # 处理客户端传来的信息
                data = item.recv(1024)
                if not data:
                    print("Client is missing....")
                    rli.remove(item)        # 从可读列表中删除此socket
                    del sock_to_queue[item] # 从字典中删除内容
                    continue
                sock_to_queue[item].put(data)
                wli.append(item)

        for item in writeable:
            data = sock_to_queue[item].get()
            if len(data) == 3 and data.startswith(b"\x05"):         # data == b"\x05\x01\x00"
                print("握手",flush=True)
                item.send(b"\x05\x00")
            elif len(data) > 3 and data.startswith(b"\x05"):  # data == b"\x05\x01\x00\x03\x0btwitter.com\x01\xbb"
                print("建立连接", flush=True)
                item.send(b"\x05\x00\x00\x01\xac\x1f\x1c\x8e\x048")
            else:
                item.send(sock_to_queue[item].get())
            wli.remove(item)

        for item in excepable:
            if item in wli:
                wli.remove(item)
            rli.remove(item)
            del sock_to_queue[item]


if __name__ == "__main__":
    main()