from posixpath import split
import socket
from time import sleep
import os

PORT = 1240
client = ''
SEPARATOR = "<SEPARATOR>"

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.bind(("", PORT))

tcp.listen(1)
con, addr = tcp.accept()

print("{addr} is connected!")

def main():
    msg = con.recv(1024).decode('utf-8')
    bufferSize, file, size = msg.split(SEPARATOR)
    print("Tamanho do buffer", bufferSize)
    print("Nome do arquivo", file)
    print("Tamanho do arquivo enviado", size, " bits")
    try:
        if os.path.exists(file):
            os.remove(file)
        arq = open(file, 'wb')
        while True:
            bytesRecv = con.recv(int(bufferSize))     
            if not bytesRecv:
                break
            arq.write(bytesRecv)
        print("Tamanho do arquivo recebido: ", (os.path.getsize(file) * 8), " bits")
        arq.close()
    except Exception as e:
        print(e)
        pass
    con.close()

main()