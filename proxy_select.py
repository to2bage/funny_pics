import select
import socket
import queue
import struct

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
                # print("建立连接", flush=True)
                # item.send(b"\x05\x00\x00\x01\xac\x1f\x1c\x8e\x048")
                # data = b"0x05 0x01 0x00 0x01 0x7f 0x00 0x00 0x01 0x1f 0x40"
                addr_type = data[3]
                if addr_type == 1:
                    # addr_ip = sock.recv(4)
                    addr_ip = data[4:8]
                    remote_addr = socket.inet_ntoa(addr_ip)
                    print(remote_addr)
                elif addr_type == 3:
                    # addr_len = int.from_bytes(sock.recv(1), byteorder='big')
                    addr_len = int.from_bytes(data[4], byteorder = "big")
                    # remote_addr = sock.recv(addr_len)
                    remote_addr = data[5:5 + addr_len]
                elif addr_type == 4:
                    # addr_ip = sock.recv(16)
                    addr_ip = data[4: 20]
                    remote_addr = socket.inet_ntop(socket.AF_INET6, addr_ip)
                else:
                    return
                # DST.PORT
                # remote_addr_port = struct.unpack('>H', sock.recv(2))
                remote_addr_port = struct.unpack('>H', data[-2:])

                # 返回给客户端 success
                reply = b"\x05\x00\x00\x01"
                reply += socket.inet_aton('0.0.0.0') + struct.pack(">H", 8888)
                item.send(reply)
                print("建立连接", flush=True)
                # 建立远程连接
                # 拿到 remote address 的信息后，建立连接
                try:
                    remote = socket.create_connection((remote_addr, remote_addr_port[0]))
                    # remote = socket.socket()
                    # remote.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    # remote.setblocking(False)
                    # remote.bind((remote_addr, remote_addr_port[0]))
                    # remote.listen(5)
                except socket.error as e:
                    print(e)
                    continue
                remote.setblocking(False)
                rli.append(remote)
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