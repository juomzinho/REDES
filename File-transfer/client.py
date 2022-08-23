import socket
from time import sleep
import threading

HOST = input("Insira o ip no qual deseja se conectar: ")
PORT = input("Insira a porta: ")
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

arq = open("file_output.txt", 'wb')

def recvMsg():
    # while True:

    msg = tcp.recv(1500)
    if not msg:
        return
    arq.write(msg)
        
    # print("Server: ", msg)
    sleep(0.1)
    arq.close()

def main():
    global HOST
    global PORT

    try: 
        dest = (HOST, int(PORT))
        tcp.connect(dest)
    except Exception as e:
        print(e)
        return

    threading.Thread(target=recvMsg).start()

    while True:
        msg = input()
        tcp.send(bytes(msg, "utf8"))
        sleep(0.1)




main()