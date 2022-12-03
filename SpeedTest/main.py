from speedtestUDP import mainUDP
from speedTestTCP import mainTCP
import os

while True:
    op = int(input("-------- Teste de Velocidade -------- \nEscolha o protocolo:\n1 - TCP\n2 - UDP\n3 - Sair\n"))
    os.system('clear')
    ip = input("Insira o IP: ")


    if(op == 1):
        os.system('clear')
        mainTCP(ip)
    elif(op ==  2):
        os.system('clear')
        mainUDP(ip)
    elif(op  == 3):
        exit()
    else:
        os.system('clear')
        print("Opção não encontrada")