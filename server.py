#!/usr/bin/env python3

import socket
import threading
import os
import time

PORTA = 18
SERVER = 'localhost'
ADDR = (SERVER, PORTA)
HEADER = 64
FORMAT = 'utf-8'

DISCONNECT = ':D'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handler(conn, addr):
    print(f'[NOVA CONEXÂO]: {addr} se conectou!')

    conectado = True
    while conectado:
        msg_length = conn.recv(HEADER).decode(FORMAT)

        if not msg_length:  # Verifica se a mensagem está vazia, o que indica uma desconexão inesperada
            print(f'[CONEXÃO ENCERRADA]: {addr}')
            break

        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        if msg == DISCONNECT:
            conectado = False

        print(f'[{time.ctime()}][{addr}]: {msg}')
        conn.send('msg recebida'.encode(FORMAT))

    conn.close()

def start():
    server.listen()
    print(f'O servidor está no endereço {SERVER}')
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handler, args=(conn, addr))
        thread.start()
        print(f'Conexões ativas: {threading.active_count() - 1}')

print('Iniciando o servidor ...')
print('--------------------------')
start()