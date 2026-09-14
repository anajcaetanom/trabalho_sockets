#####################################################
#													#
# Título do trabalho: Trabalho de Sockets			#
#		  Disciplina: Redes de Computadores PPComp	#
#													#
#####################################################

import socket
import sys

from ClientUtil import *
from Config import *
from Message import *

deviceID = None

####################
# Inicializando... #
####################
if __name__ == '__main__':
	print('Inicializando cliente: Sensor de Temperatura...')
	try:
		connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		destination = (SERVIDOR, PORTA)
		connection.connect(destination)
	except:
		print(f'Falha ao tentar se conectar com o servidor {SERVIDOR} porta {PORTA}')
		sys.exit()
	device = DeviceClient(connection, NUM_TERMOMETRO)
	roomDict = ClientRegister(device)
	if roomDict != None:
		deviceID, roomID, roomName = SelectRoom(device, roomDict)
		if deviceID != None:
			lastSensorValue = None
			while True:
				print(f'\n==> Ambiente [{roomID}] {roomName}')
				print ('Para sair digite "sair"')
				sensorValue = input('Temperatura lida no sensor: ')
				if sensorValue == 'sair': 
					break
				sensorValue = sensorValue.replace(",",".")
				try:
					floatSensorValue = float(sensorValue)
					if floatSensorValue != lastSensorValue:
						lastSensorValue = floatSensorValue
						msg = MessageSensor()
						connection.send(msg.pack(deviceID, floatSensorValue))
						print(f'Meu ID={deviceID}')
						print('Enviando temperatura ' + msg.toString())
						print('Aguardando confirmação...')
						msg = ReceiveMessage(connection, device)
						if(msg.code == MSG_STATUS and msg.status == LEITURA_RECEBIDA):
							print('Leitura recebida pelo servidor!!!')
						else:
							print(f'Falha, status = {msg.status}')
				except:
					print('Temperatura inválida')
		connection.close()
