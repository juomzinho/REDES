import socket
from time import sleep, time
import os
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

HOST = input("Insira o ip no qual deseja se conectar: ")
PORT = input("Insira a porta: ")
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SEPARATOR = "<SEPARATOR>"
bufferSize = int(input("Insira o tamanho do buffer: "))

def regexTime(num):
    string = str(num)
    newString = ''
    value = len(string)
    for i in range(0, len(string)):
        if((value - i) == 2):
            newString += ','
        if((value - i) == 5):
            newString += '.'
        # if((value - i) == 8):
        #     newString += '.'
        if((value - i) == 11):
            newString += '.'
        if((value - i) == 14):
            newString += '.'
        newString += string[i]
    return newString


def sendFile(file, ):
    i = 0
    formatedSize = '{:n}'.format(os.path.getsize(file) * 8)
    size = (os.path.getsize(file) * 8)
    print("Tamanho do arquivo a ser enviado: ", formatedSize, "bits")
    tcp.send(f"{str(bufferSize)}{SEPARATOR}{file}{SEPARATOR}{formatedSize}".encode('utf-8'))
    sleep(5)
    with open(file, 'rb') as arq:
        inicio = time()
        while True:
            bytesToSend = arq.read(bufferSize)
            if not bytesToSend:
                fim = time()
                break
            tcp.sendall(bytesToSend)
            i += 1

    tempo = size / (fim - inicio)
    print("Tempo de transmissão:", regexTime(tempo), "bits/seg")
    print("Total de pacotes enviados: ", i)

    tcp.close()
    return


def main():
    global HOST
    global PORT

    try: 
        dest = (HOST, int(PORT))
        tcp.connect(dest)
    except Exception as e:
        print(e)
        return

    file = input("Insira o arquivo: ")
    sendFile(file)

main()