import socket
import time
from urllib.parse import urlparse
from urllib.parse import urlunparse

"""
GET http://www.sina.com.cn/ HTTP/1.1
Host: www.sina.com.cn
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Cookie: UOR=,www.sina.com.cn,; SGUID=1510895799626_94484165; SINAGLOBAL=58.243.254.140_1510895800.333379; ULV=1511315145861:3:3:2:101.132.181.60_1511315143.883123:1511248073150; FTAPI_BLOCK_SLOT=FUCKIE; FTAPI_PVC=1028102-3-ja3ypnhi|1006766-18-ja3yq1de; FTAPI_ST=FUCKIE; lxlrttp=1511273241; SUB=_2AkMtUv_1f8NxqwJRmPEVzGjgZYR-yQnEieKbDg4uJRMyHRl-yD9jqkMitRBJUGFHn42FoDWh3Jvff9wnPdjdnw..; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9Whx_6.fvPcnU--UMbICy2mw
Connection: keep-alive
Upgrade-Insecure-Requests: 1
"""
def parse_header(headers):
    request_lines = headers.split("\n")
    first_line = request_lines[0].split(" ")
    method = first_line[0]
    full_path = first_line[1]
    version = first_line[2]

    scm, netloc, path, params, query, fragment = urlparse(full_path, "http")
    # 如果netloc中有":", 就指定端口号; 没有则为默认的80
    idx = netloc.find(":")
    if idx >= 0:
        address = netloc[:idx], int(netloc[idx + 1:])
    else:
        address = netloc, 80
    return method, version, scm, address, path, params, query, fragment

def handler_connection(conn):
    data = conn.recv(1024)
    # print(data.decode("utf-8"))
    msg = data.decode("utf-8")
    method, version, scm, address, path, params, query, fragment = parse_header(msg)
    path = urlunparse(("","", path, params, query, ""))
    #
    request_lines = msg.split("\n")
    req_headers = " ".join([method, path, version]) + "\n" + "\n".join(request_lines[1:])
    #
    if req_headers.find("Connection") >= 0:
        req_headers = req_headers.replace("keep-alive", "close")
    else:
        req_headers += "Connection: close\n"
    req_headers += "\n"   # null row
    # 建立远程的连接
    remote = socket.socket()
    try:
        remote.connect(address)
    except socket.error as e:
        # conn.sendall("HTTP/1.1" + str(e[0]) + "Fail\n\n")
        conn.close()
        remote.close()
    else:
        remote.sendall(req_headers.encode("utf-8"))

    # 转手数据
    while True:
        try:
            buf = remote.recv(8129)
            conn.send(buf)
            # print(buf)
        except:
            buf = None
        # finally:
        #     if not buf:
        #         remote.close()
        #         break
        #     conn.sendall(buf)
        #     conn.close()


def main():
    proxy = socket.socket()
    proxy_addr = ("0.0.0.0", 7777)
    proxy.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    proxy.bind(proxy_addr)
    proxy.listen(125)
    print("Server is listening...")

    while True:
        conn, addr = proxy.accept()
        print("Welcome %s:%s" % (str(addr[0]), str(addr[1])))
        handler_connection(conn)
            

        # time.sleep(120000)

if __name__ == "__main__":
    main()