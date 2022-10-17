import socket
import sys
from time import sleep, time
import os
import locale

HOST = ''
PORT = 1240
BUFFER = 1000

SEPARATOR = "<SEPARATOR>"
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

class UDPFileTransfer:

    def initialConfigs():
        global HOST, PORT, udp, BUFFER
       
        if len(sys.argv) == 3:
            HOST = sys.argv[1]
            PORT = int(sys.argv[2])
        else:
            print("Erro: adicionar parametros na execução do programa  ")
            exit(1)

        Option = int(input('Selecione buffer \n1 - 1000 \n2 - 1500\n'))
        if Option == 2:
            BUFFER = 1500
        elif Option != 1:
            print("Opção inválida!")
            exit()


        print("Host: ",HOST, ",Porta: ", PORT, ',Buffer: ', BUFFER)

        try: 
            addr = (HOST, PORT)

            file = input("Insira o arquivo a ser enviado: ")
            size = os.path.getsize(file)

            udp.sendto(str(os.path.basename(file)).encode('ascii'), addr)
            sleep(0.5)
            udp.sendto(str(BUFFER).encode('ascii'), addr)
            sleep(0.5)
            udp.sendto(str(size).encode('ascii'), addr)

            cont = 0
            window = int(input("Insira a janela 2 ou 4: "))
            if window != 2 and window != 4:
                print("Janela inválida!")
                exit()

            with open(file, "rb") as arq:
                start = time()
                packageToSend = arq.read(BUFFER)
                while packageToSend:
                    if udp.sendto(packageToSend, addr):
                        packageToSend = arq.read(BUFFER)
                        cont += 1
                    if cont == 2:
                        sleep(0.05)
                        cont = 0
                close = time()

                print("Janela de transmissão: ", window)
                formatedSize = locale.format_string('%.3f',arq.tell(), grouping=True)
                print("Número de pacotes enviados: ",arq.tell() // BUFFER + 1)
                print("Tamanho do arquivo: ", formatedSize)
                print("Tempo de transmissão: ", close - start)

            arq.close()


            
        except Exception as e:
            print(e)
            return

udpFileTransfer = UDPFileTransfer()

UDPFileTransfer.initialConfigs()