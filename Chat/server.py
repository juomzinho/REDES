from nis import cat
import socket
from sys import orig_argv
import threading

HOST = 'localhost'
PORT = 1023

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.bind((HOST, PORT))

def sendMsg(con):
    while True:
        msg = input()
        try:
            con.send
        except Exception as e:
            print(e)

def main():
    tcp.listen(1)
    con, addr = tcp.accept()
    print("Conectado")
    threading.Thread(target=sendMsg, args=con)
    

main()