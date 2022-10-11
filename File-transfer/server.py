from posixpath import split
import socket
from time import sleep
import os
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

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
    print("Tamanho do arquivo enviado", size, "bits")
    try:
        if os.path.exists(file):
            os.remove(file)
        arq = open(file, 'wb')
        while True:
            bytesRecv = con.recv(int(bufferSize))     
            if not bytesRecv:
                break
            arq.write(bytesRecv)
        formated = locale.format_string('%.3f',os.path.getsize(file) * 8, grouping=True)
        print("Tamanho do arquivo recebido:", formated, "bits")
        arq.close()
    except Exception as e:
        print(e)
        pass
    con.close()

main()