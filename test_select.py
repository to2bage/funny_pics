import select
import socket
import queue

server = socket.socket()
addr = ("0.0.0.0", 7777)
server.bind(addr)
server.setblocking(False)
server.listen(5)

msg_dic = {}

inputs = [server]
outputs = []

while True:
    readable, writeable, exceptable = select.select(inputs, outputs, inputs)
    for r in readable:
        if r is server:
            conn, caddr = r.accept()
            inputs.append(conn)
            msg_dic[conn] = queue.Queu()
        else:
            data = r.recv(1024)
            msg_dic[r].put(data)
            outputs.append(r)

    for w in writeable:
        w.send(msg_dic[w].get())
        outputs.remove(w)

    for e in exceptable:
        # 客户端断开了
        inputs.remove(e)
        if e in outputs:
            outputs.remove(e)
        del msg_dic[e]
