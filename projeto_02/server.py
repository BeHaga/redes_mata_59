# TODO
#  - criar um servidor para implementar as funcionalidades e requisitos do projeto

import socket

def main():
    #.AF_INET para comunicação baseada em IPs no formato protocolo IPv4
    #.SOCK_STREAM implementação de socket TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #.bind() faz associação do socket com IP e Porta
    server_socket.bind(("0.0.0.0", 12345))
    #.listen() define o tamanho da fila de conexões pendentes, até começar a recusar novas solicitações
    server_socket.listen(5)  # Aguarda até 5 conexões
    print("Servidor iniciado. Aguardando conexões...")

    while True:
        #addr é uma tupla
        client_socket, addr = server_socket.accept()
        print(f"Conexão estabelecida com {addr}")
        #.send() envio de mensagem ao cliente em formato de bytes
        client_socket.send(b"Bem-vindo ao servidor!")
        #.close() é utilizado para liberar recursos do sistema e informar ao cliente que a comunicação com o servidor foi encerrada
        client_socket.close()

if __name__ == "__main__":
    main()

#indo para a parte de autenticação do servidor, solicitando ao usuário login e registro
users = {"admin": "password"}  # Dicionário simples para autenticação

def authenticate(client_socket):
    #Lembrando que bytes não aceita caracteres pt-br
    client_socket.send(b"Digite o nome de usuario: ")
    username = client_socket.recv(1024).decode()
    client_socket.send(b"Digite a senha: ")
    password = client_socket.recv(1024).decode()

    if username in users and users[username] == password:
        client_socket.send(b"Autenticado com sucesso!")
        print(f"Usuário {username} autenticado com sucesso!")
        return True
    else:
        #Lembrando que bytes não aceita caracteres pt-br
        client_socket.send(b"Falha na autenticacao!")
        print(f"Tentativa de login falhou para o usuário {username}.")
        return False
    
#adição de threads para possibilitar que vários clientes se conectem simultaneamente
import threading

def handle_client(client_socket, addr):
    print(f"Conexão estabelecida com {addr}")
    if authenticate(client_socket):        
        #Lembrando que bytes não aceita caracteres pt-br
        client_socket.send(b"Voce agora esta conectado!")
    client_socket.close()

while True:
    client_socket, addr = server_socket.accept()
    thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    thread.start()