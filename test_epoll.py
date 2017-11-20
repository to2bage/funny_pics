import socket
import select
import queue

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_address = ("0.0.0.0", 9999)
server.bind(server_address)
server.listen(5)
server.setblocking(False)
print("Server is listening....")

timeout = 10
# 新建epoll事件对象, 后续要监控的事件, 添加到其中
epoll = select.epoll()
# 添加服务器socket的fd, 到等待读事件集合
epoll.register(server.fileno(), select.EPOLLIN)
# 每一个连接的消息字典{socket: 队列}
message_queues = {}

fd_to_socket = {server.fileno(): server,}


while True:
    print("等待活动连接......")
    # 轮训注册的事件集合
    events = epoll.poll(timeout)
    if not events:
        print("epoll 超时无活动连接, 重新轮询...")
        continue
    print("有%d个新事件, 开始处理......" % len(events))

    for fd, event in events:
        sock = fd_to_socket[fd]
        # 可读事件
        if event & select.EPOLLIN:
            # 如果sock是服务器, 表示有新的连接
            if sock is server:
                conn, addr = sock.accept()
                print("Welcome %s:%s" % (str(addr[0]), str(addr[1])))
                conn.setblocking(False)
                # 注册新连接的fd到等待读事件集合
                epoll.register(conn.fileno(), select.EPOLLIN)
                fd_to_socket[conn.fileno()] = conn 
                message_queues[conn] = queue.Queue()
            # 否则, 为客户端发送的数据
            else:
                data = sock.recv(1024)
                if data:
                    print("Recive From Client[%s]:>>> %s" % (sock.getpeername, data.decode("utf-8")))
                    message_queues[sock].put(data)
                    # 修改读取到消息的连接到等待写集合
                    epoll.modify(fd, select.EPOLLOUT)
        # 可写事件
        elif event & select.EPOLLOUT:
            try:
                msg = message_queues[sock].get()
            except Exception as e:
                print(e)
                # 修改发出消息的连接到等待读集合
                epoll.modify(fd, select.EPOLLOUT)
            else:
                sock.send(msg)

        # 关闭事件
        elif event & select.EPOLLHUP:
            epoll.unregister(fd)
            fd_to_socket[fd].close()
            del fd_to_socket[fd]

epoll.unregister(server.fileno())
epoll.close()
server.close()

