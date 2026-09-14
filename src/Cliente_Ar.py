


import socket
import sys

from ClientUtil import *
from Config import *

if __name__ == '__main__':
    print('Inicializando cliente: Ar Condicionado Inteligente')
    try:
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        destination = (SERVIDOR, PORTA)
        connection.connect(destination)
    except:
        print(f'Falha ao tentar se conectar com o servidor {SERVIDOR} porta {PORTA}')
        sys.exit()

    device = DeviceClient(connection, NUM_AR)
    roomDict = ClientRegister(device)

    if roomDict != None:
        deviceID, roomID, roomName = SelectRoom(device, roomDict)
        if deviceID != None:
            while True:
                print(f'\n==> Ambiente [{roomID}] {roomName}')
                msg = ReceiveMessage(connection, device)
                if (msg.code == MSG_AR):
                    print('Acionamento recebido do servidor!!!')
                    print('#####################################')
                    if msg.action == AR_LIGADO:
                        print('            AR CONDICIONADO LIGADO')
                    elif msg.action == AR_DESLIGADO:
                        print('            AR CONDICIONADO DESLIGADO')
                    else:
                        print(f'Ação inválida: {msg.action}')
                    print('#####################################')
                    msg = MessageStatus()
                    connection.send(msg.pack(deviceID, ACAO_EXECUTADA))
                else:
                    print('Mensagem inválida code:', msg.code)
        connection.close()