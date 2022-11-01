import socket
import locale
from time import sleep, time
import os
import sys
from select import select

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

class UDPFileTrasnfer:
    def __init__(self):
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if len(sys.argv) == 3:
            self.host = ''
            self.port = int(sys.argv[2])
            self.addr = (self.host, self.port)
            self.buffer = 1000
            self.sep = "<SEPARATOR>"
        else:
            print("Erro: adicionar parametros na execução do programa  ")
            exit(1)

    def recv(self):
        self.udp_socket.bind(('', self.port))

        pacotes_recebidos = 0
        tamanho_pacote_recebido = 0
        pacotes = []

        data, addr = self.udp_socket.recvfrom(1024)
        print(data)
        dados = data.decode().split(self.sep)
        arquivo = dados[0]
        tamanho = int(dados[1])
        self.buffer = int(dados[2])
        janela = int(dados[3])

        self.udp_socket.settimeout(0.02)

        if os.path.exists(arquivo):
            os.remove(arquivo)

        with open(arquivo, 'wb') as arq:
            while True:
                if len(pacotes) == janela:
                    for i in range(janela):
                        arq.write(pacotes[i])
                    pacotes = []
                    pacotes_recebidos += janela
                try:
                    data, addr = self.udp_socket.recvfrom(self.buffer)
                    try:
                        if data.decode() == 'fim':
                            break
                    except:
                        pass
                    if len(data) == 0:
                        self.udp_socket.sendto("erro".encode(), addr)
                        pacotes = []
                    else:
                        self.udp_socket.sendto("recebido".encode(), addr)
                        pacotes.append(data)
                    data = ''
                except Exception as e:
                    self.udp_socket.sendto("erro".encode(), addr)
                    pacotes = []
            if len(pacotes) > 0:
                print(len(pacotes))
                pacotes_recebidos += len(pacotes)
                for i in range(len(pacotes)):
                    arq.write(pacotes[i])
            arq.close()
        
        print("Pacotes recebidos: ", pacotes_recebidos)
        self.udp_socket.close()
        

        
        
udp = UDPFileTrasnfer()
udp.recv()