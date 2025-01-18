# TODO
#  - criar um servidor para implementar as funcionalidades e requisitos do projeto

import socket
#adição de threads para possibilitar que vários clientes se conectem simultaneamente
import threading
from crypto import AES

active_connections = {}  # Dicionário para armazenar conexões ativas
clients_aes_keys = {}

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
    aes_key = client_socket.recv(64)
    aes = AES(key=aes_key)
    clients_aes_keys[addr] = aes_key

    while True:
        encrypted_command = client_socket.recv(1024)
        if not encrypted_command:
            continue
        command = aes.decrypt(encrypted_command)

        if command == "autenticar":
            print("Encaminhando cliente para autenticação")
            if not authenticate(client_socket, addr):
                break
        elif command == "cadastrar":
            register(client_socket, addr)
        elif command == "sair":
            client_socket.send(aes.encrypt("Conexao com o servidor encerrada!"))
            break
        else:
            client_socket.send(aes.encrypt("Opcao invalida."))

#indo para a parte de autenticação do servidor, solicitando ao usuário login e registro
def authenticate(client_socket, addr):
    print("Cliente chegou na autenticação")
    aes = AES(key=clients_aes_keys[addr])
    username = aes.decrypt(client_socket.recv(1024))
    password = aes.decrypt(client_socket.recv(1024))

    if username in users and users[username] == password:
        active_connections[username] = client_socket  # Armazena socket em dicionário separado
        client_socket.send(aes.encrypt("Autenticado com sucesso!"))
        print(f"Usuário {username} autenticado com sucesso!")
        return chat(client_socket, addr, username)
    else:
        client_socket.send(aes.encrypt("Falha na autenticacao!"))
        print(f"Tentativa de login falhou para o usuário {username}.")
        client_socket.close()

def register(client_socket, addr):
    aes = AES(key=clients_aes_keys[addr])
    new_username = aes.decrypt(client_socket.recv(1024))
    new_password = aes.decrypt(client_socket.recv(1024))

    if new_username in users:
        client_socket.send(aes.encrypt("Usuario ja existe!"))
        register(client_socket, addr)
    else:
        users[new_username] = new_password
        save_users(users)
        client_socket.send(aes.encrypt("Usuario cadastro com sucesso!"))
        authenticate(client_socket, addr)

#após autenticação, o cliente é liberado para utilizar o chat
def chat(client_socket, addr, sender):
    while True:        
        #recebe a mensagem do cliente
        aes = AES(key=clients_aes_keys[addr])
        message = aes.decrypt(client_socket.recv(1024))

        if message.startswith("/p") and message.count(" ") >= 2:
            _, receiver, text = message.split(" ", 2)
            if receiver in users:
                send_private_message(client_socket, sender, receiver, text)
            else:
                client_socket.send(aes.encrypt("Usuário não encontrado."))

        elif message.startswith("/file"):
            _, receiver, file_name, file_size = message.split(" ", 3)
            file_size = int(file_size)
            receive_file(client_socket, sender, receiver, file_name, file_size)

        elif message.startswith("/exit"):
            print(f"O usuário {sender} {addr} encerrou sua conexão com o servidor")
            del active_connections[sender]
            return False
        else:
            client_socket.send(aes.encrypt("Digite um comando válido."))


        print(f"Mensagem recebido do usuário {addr}")
        
        #Lembrando que bytes não aceita caracteres pt-br
        response = f"\n Servidor recebeu a sua mensagem que veio escrito '{message}' \n"
        client_socket.send(aes.encrypt(response))

def send_private_message(client_socket, sender, receiver, text):
    if receiver in active_connections:  # Verifica conexões ativas em vez de users
        receiver_socket = active_connections[receiver]
        # Obtém o endereço remoto (raddr) do socket
        receiver_addr = receiver_socket.getpeername()
        aes = AES(key=clients_aes_keys[receiver_addr])
        mensagem = f"({sender}): {text}"
        receiver_socket.sendall(aes.encrypt(mensagem))
    else:
        client_addr = client_socket.getpeername()
        aes = AES(key=clients_aes_keys[client_addr])
        print(f"Destinatário {receiver} não existe ou não está conectado")
        aviso = "Usuário não existe ou não está conectado \n"
        client_socket.send(aes.encrypt(aviso))

def receive_file(client_socket, sender, receiver, file_name, file_size):
    if receiver in active_connections:
        receiver_socket = active_connections[receiver]
        receiver_addr = receiver_socket.getpeername()
        aes_receiver = AES(key=clients_aes_keys[receiver_addr])

        #momento que o servidor irá receber o arquivo do remetente
        file_content = b""
        while len(file_content) < file_size:
            file_content += client_socket.recv(min(file_size - len(file_content), 1024))

        #envia o arquivo ao destinatário
        header = f"/file {sender} {file_name} {file_size}"
        receiver_socket.sendall(aes_receiver.encrypt(header))
        receiver_socket.sendall(file_content)
        print(f"Arquivo '{file_name}' enviado de {sender} para {receiver}.")

    else:
        aes_sender = aes = AES(key=clients_aes_keys[client_socket.getpeername()])
        client_socket.send(aes_sender.encrypt("Usuário não existe ou não está conectado."))

if __name__ == "__main__":
    main()