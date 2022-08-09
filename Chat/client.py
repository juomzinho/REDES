import socket

HOST = ''
PORT = 1032

def main():
    global HOST
    global PORT

    print("Insira o IP em que deseja se conectar")
    HOST = input()
    print("Insira a porta em que deseja se conectar")
    HOST = input()
    print(HOST)

main()