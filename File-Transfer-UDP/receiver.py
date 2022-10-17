from select import select
import socket
import sys
from time import sleep, time
import os
import locale
import select

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

HOST = ''
PORT = 1240
BUFFER = 1000

SEPARATOR = "<SEPARATOR>"
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

class UDPFileTransfer:

    def initialConfigs():
        global HOST, PORT, udp, BUFFER
       
        if len(sys.argv) == 3:
            HOST = sys.argv[1]
            PORT = int(sys.argv[2])
        else:
            print("Erro: adicionar parametros na execução do programa  ")
            exit(1)

        try:
            udp.bind(('', PORT))

            data, addr = udp.recvfrom(1024)
           
            file = ''
            size = 0
            BUFFER = 1000
            if data:
                file = data.decode('ascii')
                print(f"Arquivo: {file}")
            data, addr = udp.recvfrom(1024)
            BUFFER = int(data.decode('ascii'))
            data, addr = udp.recvfrom(1024)
            size = int(data.decode('ascii'))

            if os.path.exists(file):
                os.remove(file)

            print(size)
            arq = open(file, "wb")
            start = time()

            while True:
                ready = select.select([udp], [], [], 3)
                if ready[0]:
                    data, addr =  udp.recvfrom(BUFFER)
                    arq.write(data)
                else:
                    break
            

            formatedSize = locale.format_string('%.3f',arq.tell(), grouping=True)
            print("Tamanho do arquivo recebido: ", formatedSize)
            print("Numero de pacotes recebidos: ", arq.tell() // BUFFER + 1)
            
        except Exception as e:
            print(e)

UDPFileTransfer.initialConfigs()