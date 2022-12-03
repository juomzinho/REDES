import time
import socket
import random
import select
from traceback import print_tb
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def teste(op, IP):
    PORT_S = 8000
    teste = "teste de rede *2022*"
    msgsize = len(teste)
    testmessage = ''
    for i in range(0, 500, msgsize):
       testmessage = testmessage + teste
    
    #Lado emissor
    if op == 1:
        #Criacao de socket que envia dados
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        bytes_enviados = 0
        pacotes = 0
        print('\nIniciando teste de upload...')
        s.sendto(bytes('teste-upload', 'utf8'), (IP, PORT_S)) #notifica início do envio
        inicio = time.time()
        while time.time() < inicio+20:
            try:
                bytes_sent = s.sendto(bytes(testmessage, 'utf-8'), (IP, PORT_S))
                bytes_enviados += bytes_sent
                pacotes += 1

            except:
                print("\nErro em teste de upload")      #notifica algo errado no geral e interrompe
                break
            
        s.sendto(bytes('fim-teste-upload', 'utf8'), (IP, PORT_S)) #notifica o fim do envio
        s.sendto(bytes(str(pacotes), 'utf-8'), (IP, PORT_S))      #envia o número de pacotes enviados
        print("\nFim do teste de upload")
        tempo_total = time.time() - inicio
        velocidade =  locale.format_string('%.3f',(bytes_enviados*8)/tempo_total, grouping=True)
        velocidade_kb =  locale.format_string('%.3f',((bytes_enviados*8)/tempo_total)/1024, grouping=True)
        velocidade_mb =  locale.format_string('%.3f',((bytes_enviados*8)/tempo_total)/1048576, grouping=True)
        velocidade_gb =  locale.format_string('%.3f',((bytes_enviados*8)/tempo_total)/1073741824, grouping=True)
        bits_enviados = locale.format_string('%.3f',bytes_enviados*8, grouping=True)
        velocidade_uploadP = pacotes/tempo_total
        print(f'\nTotal de pacotes enviados: {"{:,}".format(pacotes)}\nTempo Decorrido: {tempo_total}\nVelocidade media(pacotes/s):{"{:,}".format(velocidade_uploadP)}')
        print("bits enviados: ", bits_enviados)
        print("Velocidade em Kbps: ", velocidade_kb)
        print("Velocidade em Mbps: ", velocidade_mb)
        print("Velocidade em Gbps: ", velocidade_gb)
        s.close()

        #Lado receptor
    elif op == 2:
            #Criacao e definicao de socket receptor
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.bind((IP, PORT_S))
            print("\nAguardando...")
            s.settimeout(60) #timeout caso demore para receber/nenhum dado chegue

            bytes_recebidos = 0
            pacotes_download = 0
            msg, address = s.recvfrom(500)
            msg = msg.decode('utf-8')
            if 'teste-upload' in msg:
                print('\nIniciando teste de download...')
                inicio_download = time.time()
                while True:
                    try:
                        s.setblocking(False)
                        ready = select.select([s],[],[],15)

                        if ready[0]:
                            msg, address = s.recvfrom(500)     #timeout
                        else: print("erro")
                        
                        msg = msg.decode('utf8')
                        bytes_received = len(msg)
                        bytes_recebidos += bytes_received
                        if bytes_received == 500:
                            pacotes_download += 1
                        #if not msg:
                            #break                               
                        if 'fim-teste-upload' in msg:           #confirmações de final
                            print("\nFim do teste de download")
                            break

                    except:
                        print("\nErro em teste de download")        #notifica algo errado no geral e interrompe
                        break
                try:
                    s.setblocking(False)
                    ready = select.select([s],[],[],15)

                    if ready[0]:
                       pc, address = s.recvfrom(500)      #timeout
                       if pc:
                        pacotes_upload = pc.decode('utf-8')
                    else: 
                        print("erro")
                        pacotes_upload = pacotes_download
                    
                    
                    tempo_total_download = time.time() - inicio_download
                    velocidade_download = bytes_recebidos/tempo_total_download
                    velocidade_downloadP = pacotes_download/tempo_total_download
                    velocidade =  locale.format_string('%.3f',(bytes_recebidos*8)/tempo_total_download, grouping=True)
                    velocidade_kb =  locale.format_string('%.3f',((bytes_recebidos*8)/tempo_total_download)/1024, grouping=True)
                    velocidade_mb =  locale.format_string('%.3f',((bytes_recebidos*8)/tempo_total_download)/1048576, grouping=True)
                    velocidade_gb =  locale.format_string('%.3f',((bytes_recebidos*8)/tempo_total_download)/1073741824, grouping=True)
                    bits_recebidos = locale.format_string('%.3f',bytes_recebidos*8, grouping=True)
                    lost = int(pacotes_upload) - pacotes_download       #pacotes perdidos
                    
                    if lost < 0:        #acontece de contabilizar 1 pacote enviado a mais em casos de envio ótimos (-1 perdidos), para isso retificamos para 0
                        lost = 0
                    print(f'\nTotal de pacotes recebidos: {"{:,}".format(pacotes_download)}\nTempo Decorrido: {tempo_total_download}s\nVelocidade media(pacotes/s): {"{:,}".format(velocidade_downloadP)}')
                    print("bits recebidos: ", bits_recebidos)
                    print("Velocidade Kbps: ", velocidade_kb)
                    print("Velocidade Mbps: ", velocidade_mb)
                    print("Velocidade Gbps: ", velocidade_gb)
                    print(f'\nPacotes perdidos: {"{:,}".format(lost)}')
                except Exception as e:
                    print("string nula", e)     #exceção que acontece em caso de bytes nulos/vazios que atrapalham ao receber informações
            
            else: print('Nenhum dado recebido.')

            print("\nFim dos testes")
            s.close()

    elif op == 3: #Encerrar o programa
            exit()

def mainUDP(IP):
     while True:
        print("-------- Teste de Velocidade - UDP --------\nEscolha uma opcao:")
        option = int(input("1 - Enviar pacotes de teste;\n2 - Receber pacotes de teste;\n3 - Sair.\n"))
        teste(option, IP)