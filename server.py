#!/usr/bin/env python3

############### Bibliotecas ##################

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

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Cria um socket do servidor.

server.bind(ADDR) #Liga o servidor ao endereço

conexoes = []

def handler(conn, addr):
    try:  
     print(f'[NOVA CONEXÃO]: {addr} se conectou!')

     conectado = True
     conexoes.append(conn)

     while conectado:
        
         msg_length = conn.recv(HEADER).decode(FORMAT) #Recebe o comprimento da mensagem codificado e decodifica para uma string.

         if not msg_length: #Verifica se a mensagem está vazia, o que indica uma desconexão inesperada.
             print(f'[CONEXÃO ENCERRADA]: {addr}') 
             break

         msg_length = int(msg_length)

         msg = conn.recv(msg_length).decode(FORMAT) #Recebe a mensagem do cliente com base no comprimento recebido.

         if msg == DISCONNECT: #Quando recebe a mensagem de desconexão define a conexão como False
             print(f'[CONEXÃO ENCERRADA]: {addr}') 
             conectado = False

         print(f'[{time.ctime()}][{addr}]: {msg}') #Exibe a mensagem do cliente

         # Envia a mensagem para todos os clientes
         for conexao in conexoes:
             conexao.send(f'[{time.ctime()}][{addr}]: {msg}'.encode(FORMAT))

    except Exception as e:
        print(f"Erro:{e}")

    finally:
        if conn in conexoes:
            conexoes.remove(conn)
        conn.close()        

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
