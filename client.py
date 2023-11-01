#!/usr/bin/env python3

import socket
import threading

###### Definições feitas em turma ############

HEADER = 64
PORT = 18
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = ':D'
SERVER = 'localhost'
ADDR = (SERVER, PORT)

##############################################

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Cria um socket do cliente

client.connect(ADDR) #Estabelece uma conexão com o endereço

def send(msg):
    
    message = msg.encode(FORMAT) #Codifica a mensagem

    msg_len = len(message)

    #Codifica o comprimento da mensagem como uma string
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER - len(send_len))
    ###

    #Envia o comprimento da mensagem seguido pela mensagem em si para o servidor.
    client.send(send_len)
    client.send(message)
    ###

    print(client.recv(HEADER).decode(FORMAT)) #Aguarda uma resposta do servidor

while True:
    entry = input('Sua mensagem: ')

    send(entry) #Envia a mensagem ao servidor.

    if entry == DISCONNECT_MESSAGE:
        print("Desconectando...")
        break

client.close() #Fecha a conexão




        