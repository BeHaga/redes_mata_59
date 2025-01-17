# TODO
#  - criar um servidor para implementar as funcionalidades e requisitos do projeto

import socket
#adição de threads para possibilitar que vários clientes se conectem simultaneamente
import threading

active_connections = {}  # Dicionário para armazenar conexões ativas

def main():
    #.AF_INET para comunicação baseada em IPs no formato protocolo IPv4
    #.SOCK_STREAM implementação de socket TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #.bind() faz associação do socket com IP e Porta
    server_socket.bind(("0.0.0.0", 12345))
    #.listen() define o tamanho da fila de conexões pendentes, até começar a recusar novas solicitações
    server_socket.listen(5)  # Aguarda até 5 conexões
    print("Servidor iniciado. Aguardando conexões...")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            thread.start()
    except KeyboardInterrupt:
        print("Encerrando servidor...")
    finally:
        server_socket.close()

#backup dos dados de login dos usuarios
import json
import os

def load_users():
    if os.path.exists("users.json"):
        with open("users.json", "r") as file:
            return json.load(file)
    return {}

def save_users(users):
    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)

users = load_users()

def handle_client(client_socket, addr):
    print(f"Conexão estabelecida com {addr}")

    while True:
        command = client_socket.recv(1024).decode()

        if command == "autenticar":
            print("Encaminhando cliente para autenticação")
            if not authenticate(client_socket, addr):
                break
        elif command == "cadastrar":
            register(client_socket, addr)
        elif command == "sair":
            client_socket.send(b"Conexao com o servidor encerrada!")
            break
        else:
            client_socket.send(b"Opcao invalida.")

#indo para a parte de autenticação do servidor, solicitando ao usuário login e registro
def authenticate(client_socket, addr):
    print("Cliente chegou na autenticação")
    #Lembrando que bytes não aceita caracteres pt-br
    # client_socket.send(b"Digite o nome de usuario: ")
    username = client_socket.recv(1024).decode()
    # client_socket.send(b"Digite a senha: ")
    password = client_socket.recv(1024).decode()

    if username in users and users[username] == password:
        active_connections[username] = client_socket  # Armazena socket em dicionário separado
        client_socket.send(b"Autenticado com sucesso!")
        print(f"Usuário {username} autenticado com sucesso!")
        return chat(client_socket, addr, username)
    else:
        #Lembrando que bytes não aceita caracteres pt-br
        client_socket.send(b"Falha na autenticacao!")
        print(f"Tentativa de login falhou para o usuário {username}.")
        client_socket.close()

def register(client_socket, addr):
    new_username = client_socket.recv(1024).decode()
    new_password = client_socket.recv(1024).decode()

    if new_username in users:
        client_socket.send(b"Usuario ja existe!")
        register(client_socket, addr)
    else:
        users[new_username] = new_password
        save_users(users)
        client_socket.send(b"Usuario cadastro com sucesso!")
        authenticate(client_socket, addr)

#após autenticação, o cliente é liberado para utilizar o chat
def chat(client_socket, addr, sender):
    while True:        
        #recebe a mensagem do cliente
        message = client_socket.recv(1024).decode()

        if message.startswith("/p"):
            _, receiver, text = message.split(" ", 2)
            send_private_message(client_socket, sender, receiver, text)

        elif message.startswith("/exit"):
            client_socket.close()
            print(f"O usuário {sender} {addr} encerrou sua conexão com o servidor")
            return False

        print(f"Mensagem recebido do usuário {addr}")
        
        #Lembrando que bytes não aceita caracteres pt-br
        response = f"\n Servidor recebeu a sua mensagem que veio escrito '{message}' \n"
        client_socket.send(response.encode())

def send_private_message(client_socket, sender, receiver, text):
    if receiver in active_connections:  # Verifica conexões ativas em vez de users
        receiver_socket = active_connections[receiver]
        mensagem = f"({sender}): {text}"
        receiver_socket.sendall(mensagem.encode())
    else:
        print(f"Destinatário {receiver} não existe ou não está conectado")
        aviso = "Usuário não existe ou não está conectado \n"
        client_socket.sendall(aviso.encode())

if __name__ == "__main__":
    main()