import socket
import threading
import os

# Obtém o ID do processo atual
id = os.getpid()

# Define o endereço do servidor como localhost na porta 18000
SERVIDOR = 'localhost'
PORTA = 18000
FORMATO = 'utf-8'
endereco = (SERVIDOR, PORTA)

# Cria um soquete de cliente
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect(endereco)

# Função para enviar mensagens para o servidor
def transmitir(string):
    mensagem = string.encode(FORMATO)
    tamanho_mensagem = str(len(mensagem)).encode(FORMATO)
    tamanho_mensagem += b' ' * (64 - len(tamanho_mensagem))
    socket.send(tamanho_mensagem)
    socket.send(mensagem)

# Função para ouvir mensagens do servidor
def ouvir():
    while True:
        string = socket.recv(2048).decode(FORMATO)
        if not string:
            break
        print("\n" + string)

# Início da execução do programa
if __name__ == "__main__":
    # Inicia a função 'ouvir' em uma thread separada
    servidor = threading.Thread(target=ouvir)
    servidor.daemon = True
    servidor.start()
    
    while True:
        mensagem = input('Sua mensagem: ')
        transmitir(mensagem)
        
        # Se a mensagem for ':D', fecha o soquete do cliente e encerra o programa
        if mensagem == ':D':
            socket.close()
            os.kill(id, 9)


