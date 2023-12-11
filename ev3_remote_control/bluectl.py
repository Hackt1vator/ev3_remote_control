import socket

def connect(mac:str, ch:int):
    s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    s.connect((mac,channel))
    sock = s.accept()
    print("Accepted connection from "+address)

    data = sock.recv(1024)
    print("received "+data.decode())

    buffer = None; output = None; tmp = None
    while True:
        buffer = input("# ")
        sock.send(buffer.encode())
        while True:
            tmp = sock.recv(1024).decode()
            if not tmp: break
            output += tmp
        print(str(output, "utf-8"))

def server(mac:str, ch:int):
    buffer = None; tmp = None
    s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    s.bind((mac , ch))
    s.listen(1)
    client, client_addr = s.accept()

    client.send("test".encode())
    while True:
        while True:
            tmp = client.recv(1024).decode()
            if not tmp: break
            buffer += tmp
        print(str(buffer, "utf-8"))
        buffer = input()
        client.send(buffer.encode())

#pybluez
#https://github.com/pybluez/pybluez source code to make local import tig
#https://pybricks.com/ev3-micropython/messaging.html msgserver in micropython

server("F0:57:A6:91:FB:68", 17)