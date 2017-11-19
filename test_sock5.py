import socketserver
import time
import socket


class MultiRequestHandler(socketserver.StreamRequestHandler):
    def handle(self):
        sock = self.connection
        # Sock5 握手
        data = sock.recv(262)
        print(data, flush=True)
        sock.send(b"\x05\x00")          # 无需认证

        # Sock5 建立连接
        """
        data = self.rfile.read(4)       # 只读前4个字节的数据b'\x05\x01\x00\x01'
        print("new:", data, flush=True)
        print("data[0] = ", data[0])    # data的第一个字节, 是5:int类型
        print("data[1] = ", data[1])    # data的第二个字节, 是1:int类型
        print("data[2] = ", data[2])    # data的第三个字节, 是0:int类型
        print("data[3] = ", data[3])    # data的第四个字节, 是1:int类型
        """
        data = self.rfile.read(4)        # b'\x05\x01\x00\x01    \xd0\x1f\xfe\x12\x00P'
        print("data = ", data, flush=True) # 此时data[3] == 1
        # addr_to_send = str(data[3])
        addr_to_send = b""
        addr_to_send += chr(data[3]).encode("utf-8")
        if data[3] == 1:
            # 后面有4个字节的IPv4地址
            addr_ip = self.rfile.read(4)      # 再读4个字节
            addr = socket.inet_ntoa(addr_ip)
            print(addr, type(addr))
            addr_to_send += addr.encode("utf-8")
        elif data[3] == 3:
            # 后面一个字节表示域名的长度, 紧随其后的是对应的域名
            addr_len = self.rfile.read(1)     # 再读1个字节, 获得域名的长度
            addr = self.rfile.read(ord(addr_len))
            addr_to_send += addr_len + addr
            pass
        elif data[3] == 4:
            # 后面有16个字节的IPv6地址
            pass
        addr_port = self.rfile.read(2)      # 再读取2个字节, 获得端口号
        addr_to_send += addr_port

        print("addr_to_send = ", addr_to_send, flush=True) # addr_to_send = b'\x01101.71.100.123\x00P'

        reply = b"\x05\x00\x00\x01\x00\x00\x00\x00\x10\x10"
        self.wfile.write(reply)
        print("连接建立完成")

        # 传送阶段
        from urllib import request

        #request.Request()



        time.sleep(50)

def main():
    
    server_addr = ("0.0.0.0", 9999)
    server = socketserver.ThreadingTCPServer(server_addr, MultiRequestHandler)
    server.allow_reuse_address = True           # ip地址可以重复使用
    server.serve_forever()

if __name__ == "__main__":
    main()