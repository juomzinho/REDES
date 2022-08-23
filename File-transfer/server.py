import socket
import threading
from time import sleep

HOST = input("Insira seu ip: ")
PORT = 1240
client = ''

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.bind((HOST, PORT))

tcp.listen(1)
con, addr = tcp.accept()

print("Conexão aceita")

arq = open('./download.jpeg', 'rb')
print(arq)

def recvMsg():
    while True:
        msg = con.recv(1024).decode("utf8")
        print("Client:", msg)
        sleep(0.1)

def main():
    threading.Thread(target=recvMsg).start()
    # while True:
    con.sendall(arq)
    # sleep(0.1)

main()