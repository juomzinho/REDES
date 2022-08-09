import socket
from time import sleep
import threading

HOST = 'localhost'
PORT = 1240
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)

def recvMsg():
    while True:
        msg = tcp.recv(1024).decode('utf8')
        print("Server: ", msg)
        sleep(0.1)

def main():
    global HOST
    global PORT

    print("Insira o IP em que deseja se conectar")
    HOST = input()
    print("Insira a porta em que deseja se conectar")
    HOST = input()
    print(HOST)

    tcp.connect(dest)

    threading.Thread(target=recvMsg).start()

    while True:
        msg = input()
        tcp.send(bytes(msg, "utf8"))
        sleep(0.1)




main()