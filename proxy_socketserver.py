import socketserver
import socket
import struct
import select

def handle_tcp(client, remote):
    rli = [client, remote]
    wli = []

    while True:
        readable, writeable, excepable = select.select(rli, wli, rli)
        if client in readable:
            # 客户端有新的请求
            req_data = client.recv(1024)
            remote.send(req_data)
        if remote in readable:
            # 远程服务端有响应, 发送给客户端
            reps_data = remote.recv(1024)
            client.send(reps_data)

class RequestClass(socketserver.BaseRequestHandler):
    def handle(self):
        conn = self.request
        print("Welecome %s:%s" % (str(self.client_address[0]), str(self.client_address[1])))
        # Sock5的握手
        conn.recv(1024)
        conn.send(b"\x05\x00")
        # Sock5连接
        data = conn.recv(1024)
        # 获得请求的ip地址, data = "0x05 0x01 0x00 0x01 0x7f 0x00 0x00 0x01 0x1f 0x40"
        if data[1] != 1:
            print("[%s]: TCP连接失败!!!" % self.client_address[0], flush=True)
            conn.close()
            return
        # data[3]:  0x01：IPv4 ; 0x03：域名 ; 0x04：IPv6
        if data[3] == 1:
            # IPV4
            remote_addr = socket.inet_ntoa(data[4:8])
        elif data[3] == 3:
            # 域名
            namelen = int.from_bytes(data[4], byteorder = "big")
            remote_addr = socket.inet_ntoa(data[5:5 + namelen])
        elif data[3] == 4:
            # IPV6
            remote_addr = socket.inet_ntop(socket.AF_INET6, data[4: 4 + 16])
        # 获得端口号
        remote_port = struct.unpack(">H", data[-2:])
        # 服务端确认连接请求
        msg = b"\x05\x00\x00\x01"
        conn.send(msg + socket.inet_aton("0.0.0.0") + struct.pack(">H", 8888))
        #
        print("连接完成, 请求远程地址: %s:%s" % (remote_addr, remote_port[0]))
        # 建立与远端的连接
        remote = socket.create_connection((remote_addr, remote_port[0]))
        # 调用函数
        handle_tcp(conn, remote)

def main():
    proxy_address = ("0.0.0.0", 9999)
    proxy_server = socketserver.ThreadingTCPServer(proxy_address, RequestClass)
    proxy_server.allow_reuse_address = True
    proxy_server.serve_forever()


if __name__ == "__main__":
    main()