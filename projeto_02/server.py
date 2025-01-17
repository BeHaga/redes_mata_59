# TODO
#  - criar um servidor para implementar as funcionalidades e requisitos do projeto

import socket
import threading

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
        client_socket, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

#indo para a parte de autenticação do servidor, solicitando ao usuário login e registro
users = {"admin": "password", "bh": "1234"}  # Dicionário simples para autenticação

def authenticate(client_socket):
    #Lembrando que bytes não aceita caracteres pt-br
    # client_socket.send(b"Digite o nome de usuario: ")
    username = client_socket.recv(1024).decode()
    # client_socket.send(b"Digite a senha: ")
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
        while True:        
            #recebe a mensagem do cliente
            message = client_socket.recv(1024).decode()
            if message == "sair":
                client_socket.close()
                print(f"O usuário {addr} encerrou sua conexão com o servidor")
                return False

            print(f"Mensagem recebido do usuário {addr}")
            
            #Lembrando que bytes não aceita caracteres pt-br
            response = f"Eu recebi a sua mensagem que veio escrito '{message}'"
            client_socket.send(response.encode())
    
if __name__ == "__main__":
    main()