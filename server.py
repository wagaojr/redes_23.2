#!/usr/bin/env python3

############### BIBLIOTECAS ##################

import socket
import threading
import os
import time

##############################################

###### Definições feitas em turma ############

PORTA = 18
SERVER = 'localhost'
ADDR = (SERVER, PORTA)
HEADER = 64
FORMAT = 'utf-8'
DISCONNECT = ':D'

##############################################

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Cria um socket do servidor usando a família de endereços IPv4 (AF_INET) e o protocolo TCP (SOCK_STREAM).

server.bind(ADDR) #Liga o servidor ao endereço

def handler(conn, addr):
    print(f'[NOVA CONEXÃO]: {addr} se conectou!')

    conectado = True
    while conectado:
        
        msg_length = conn.recv(HEADER).decode(FORMAT) #Recebe o comprimento da mensagem codificado e decodifica para uma string.

        if not msg_length: #Verifica se a mensagem está vazia, o que indica uma desconexão inesperada.
            print(f'[CONEXÃO ENCERRADA]: {addr}') 
            break

        msg_length = int(msg_length)

        msg = conn.recv(msg_length).decode(FORMAT) #Recebe a mensagem do cliente com base no comprimento recebido.

        if msg == DISCONNECT: #Quando recebe a mensagem de desconexão define a conexão como False
            conectado = False

        print(f'[{time.ctime()}][{addr}]: {msg}') #Exibe a mensagem do cliente

        conn.send('msg recebida'.encode(FORMAT)) #Exibe a mesma mensagem que recebeu do cliente

    conn.close() #Fecha a conexão

def start():
    
    server.listen() #Coloca o servidor no modo de escuta para aguardar as conexões dos clientes.

    print(f'O servidor está no endereço {SERVER}')

    while True:
        
        conn, addr = server.accept() #Aceita uma nova conexão de cliente

        thread = threading.Thread(target=handler, args=(conn, addr)) #Cria uma nova thread para lidar com o cliente
        thread.start()

        print(f'Conexões ativas: {threading.active_count() - 1}') #Exibe o número de conexões ativas

print('Iniciando o servidor ...')
print('--------------------------')

start()
