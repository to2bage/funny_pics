import socket

client = socket.socket()
client.connect(("101.132.181.60", 9999))

while True:
    msg = input("MSG:>>>").strip()
    client.send(msg.encode("utf-8"))
    data = client.recv(1024)
    print("Recive :", data.decode("utf-8"))

client.close()