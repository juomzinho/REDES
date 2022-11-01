import socket
import locale
from time import sleep, time
import os
import sys

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

class UDPFileTrasnfer:
    def __init__(self):
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if len(sys.argv) == 3:
            self.host = sys.argv[1]
            self.port = int(sys.argv[2])
            self.addr = (self.host, self.port)
            self.buffer = 1000
            self.sep = "<SEPARATOR>"
        else:
            print("Erro: adicionar parametros na execução do programa  ")
            exit(1)

    def send(self):
        pacotes_enviados = 0
        pacotes_perdidos = 0
        pacotes_recebidos = 0
        pacotes = []

        Option = int(input('Selecione buffer \n1 - 1000 \n2 - 1500\n'))
        if Option == 2:
            self.buffer = 1500
        elif Option != 1:
            print("Opção inválida!")
            exit()

        print("Host: ",self.host, ",Porta: ", self.port
            , ',Buffer: ', self.buffer)

        file = input("Insira o arquivo a ser enviado: ")
        size = os.path.getsize(file) * 8
        window = int(input("Insira a janela 2 ou 4: "))
        if window != 2 and window != 4:
            print("Janela inválida!")
            exit()
        
        self.udp_socket.sendto(f"{file}{self.sep}{size}{self.sep}{self.buffer}{self.sep}{window}".encode(), self.addr)
        self.udp_socket.settimeout(0.02)
        try:
            with open(file, "rb") as arq:
                pacote = arq.read(self.buffer)
                inicio = time() 
                while pacote:
                    if len(pacotes) == window:
                        try:
                            for i in range(window):
                                self.udp_socket.sendto(pacotes[i], self.addr)
                                data, addr = self.udp_socket.recvfrom(self.buffer)
                                if data.decode() == 'recebido':
                                    pacotes_recebidos += 1
                                    pacote = arq.read(self.buffer)
                                if data.decode() == 'erro':
                                    i = 0
                                    pacotes_perdidos += 1
                                pacotes_enviados += 1
                            sleep(0.02)
                        except Exception as e:
                            print("dentro", e)
                    else:
                        pacotes.append(arq.read(self.buffer))
                self.udp_socket.sendto('fim'.encode(), self.addr)
                print("saiu")
                if len(pacotes) > 0: 
                    try:
                        for i in range(window):
                            self.udp_socket.sendto(pacotes[i], self.addr)
                            data, addr = self.udp_socket.recvfrom(self.buffer)
                            if data.decode() == 'recebido':
                                pacotes_recebidos += 1
                                pacote = arq.read(self.buffer)
                            if data.decode() == 'erro':
                                pacotes_perdidos += 1
                            pacotes_enviados += 1
                    except Exception as e:
                        print("fora", e)
                fim = time()
               

                transmissao = size / (fim - inicio)
                print("Janela de transmissão: ", window)
                formatedSize = locale.format_string('%.2f',(arq.tell() * 8), grouping=True)
                print("Número de pacotes enviados: ",arq.tell() // self.buffer + 1)
                print("Número de pacotes enviados: ",pacotes_enviados)
                print("Número de pacotes perdidos: ", pacotes_perdidos)
                print("Tamanho do arquivo: ", formatedSize)
                formatedSize = locale.format_string('%.2f', transmissao, grouping=True)
                print("Tempo de transmissão: ", formatedSize)

            arq.close()
            self.udp_socket.close()
        except Exception as e:
            print("exit:",  e)
            exit()
        
udp = UDPFileTrasnfer()
udp.send()