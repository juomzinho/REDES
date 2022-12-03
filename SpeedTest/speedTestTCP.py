import time
import socket
import random
from traceback import print_tb
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def mainTCP(IP):
    PORT_S = 8000
    teste = "teste de rede *2022*"
    msgsize = len(teste)
    testmessage = ''
    for i in range(0, 500, msgsize):
       testmessage = testmessage + teste
        
    print("Escolha uma opcao:")
    op = int(input("1 - Enviar;\n2 - Receber;\n"))
    
    while True:
        if op == 1:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((IP, PORT_S))
                timeout = 20
                
                bytes_enviados = 0
                pacotes = 0
                            
                s.send(bytes('upload', 'utf8'))
                print('\nIniciando teste de upload...')
                start_upload = time.time()
                
                while time.time() < start_upload+timeout:
                    try:
                        msg = bytes((testmessage), 'utf8')
                        envio = s.send((msg))
                        bytes_enviados += envio 
                        pacotes += 1
                                
                    except:
                        print("Erro em teste de upload")
                        break
                
                s.send(bytes('fim-teste-upload', 'utf8'))
                
                time.sleep(1)
                
                s.send(bytes(f'{pacotes}', 'utf8'))
                
                
                bits_enviados = bytes_enviados * 8
                pacotes_segundo = pacotes/20
                velocidade_upload = (bits_enviados)/20
                
                print(f'\nTotal de pacotes enviados: {pacotes}' )
                print(f'Pacotes enviados por segundo: {pacotes_segundo}')
                formated_bits_enviados = locale.format_string('%.3f',bits_enviados, grouping=True)
                formated_speed_upload = locale.format_string('%.3f',velocidade_upload, grouping=True)
                formated_speed_upload_kb = locale.format_string('%.3f',velocidade_upload / 1024, grouping=True)
                formated_speed_upload_mb = locale.format_string('%.3f',velocidade_upload / 1048576, grouping=True)
                formated_speed_upload_gb = locale.format_string('%.3f',velocidade_upload / 1073741824, grouping=True)
                print(f'Total de bits enviados: {bits_enviados}\nbits enviados: {formated_bits_enviados}')
                print(f'Velocidade media(bits/s): {formated_speed_upload}')
                print(f'Velocidade media(Kbits/s): {formated_speed_upload_kb}')
                print(f'Velocidade media(Mbits/s): {formated_speed_upload_mb}')
                print(f'Velocidade media(Gbits/s): {formated_speed_upload_gb}')
                print('\nFim teste de upload...')
                
                s.send(bytes('fim-testes', 'utf8'))
                    
                s.close()
                exit()
        

          
        
        elif op == 2:
            pacotes = 0
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((IP, PORT_S))
            s.listen(1)
            print("Aguardando conexao...")

            conexao, address = s.accept()
            print("Conexao aceita em: {}" .format(address))

            bytes_recebidos = 0
            pacotes_upload = 0
            
            msg = conexao.recv(500)
            msg = msg.decode('utf8')

            if 'upload' in msg:
                print('\nIniciando teste de download...')
                start_upload = time.time()

                while True:
                    try:
                        msg = conexao.recv(500)
                        msg = msg.decode('utf8')
                        bytes_received = msg.__len__()
                        bytes_recebidos += bytes_received
                        if(bytes_received == 500):
                            pacotes_upload += 1
                        if 'fim-teste-upload' in msg:
                            print("Fim do teste de download")
                            break

                    except:
                        print("Erro em teste de upload")
                        break
                
            
                tempo_total = time.time() - start_upload
                bits_recebidos = bytes_recebidos*8
                velocidade = (bits_recebidos)/tempo_total
                
                msg = conexao.recv(50).decode('utf8')
                pacotes_enviados = msg
                pacotes_perdidos = 0
                pacotes_segundo = pacotes_upload/20

                print(f'Total de pacotes recebidos: {pacotes_enviados}\nTotal de pacotes enviados: {pacotes_enviados}')
                print(f'Pacotes recebidos por segundo: {pacotes_segundo}')
                print(f'Total de pacotes perdidos: {pacotes_perdidos}\nTempo Decorrido: {tempo_total}s\n')   
                formated_bits_enviados = locale.format_string('%.3f',bits_recebidos, grouping=True)
                formated_speed_download = locale.format_string('%.3f',velocidade, grouping=True)
                formated_speed_download_kb = locale.format_string('%.3f',velocidade / 1024, grouping=True)
                formated_speed_download_mb = locale.format_string('%.3f',velocidade / 1048576, grouping=True)
                formated_speed_download_gb = locale.format_string('%.3f',velocidade / 1073741824, grouping=True)
                print(f'bits recebidos: {formated_bits_enviados}')
                print(f'Velocidade media(bits/s): {formated_speed_download}')
                print(f'Velocidade media(Kbits/s): {formated_speed_download_kb}')
                print(f'Velocidade media(Mbits/s): {formated_speed_download_mb}')
                print(f'Velocidade media(Gbits/s): {formated_speed_download_gb}')


            end = conexao.recv(1024).decode('utf8')
            if not 'fim-testes' in end:
                time.sleep(1)
            print("\nFim dos testes")
            
            conexao.close()
            s.close()
            exit()
  