# TODO
#  - conexao com o servidor para implementar as funcionalidades e requisitos do projeto

# - cada cliente se comunica com o servidor, que gerenciara a comunicacao entre clientes
# - cada cliente deve se cadastrar junto ao servidor como um usuario
# - cada cliente deve poder se comunicar com outro cliente usando o nome de usuario (semelhante ao que ocorre no WhatsApp atraves do numero de telefone)
# - (OPCIONAL) clientes podem se juntar a grupos multicast (semelhante ao que ocorre no whatsapp)

import socket
import threading

def main():
    #.AF_INET para comunicação baseada em IPs no formato protocolo IPv4
    #.SOCK_STREAM implementação de socket TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #esse IP é o padrão de loopback, utilizado em desenvolvimento local
    client_socket.connect(("127.0.0.1", 12345))
    
    print("Seja bem vindo! Escolha uma das opções a seguir: ")

    while True:
        print("1 - Autenticar")
        print("2 - Cadastrar novo usuário")
        print("3 - Sair")
        option = input("Digite o número da opção desejada: ")

        if option == "1":
            client_socket.send(b"autenticar")
            authenticate(client_socket)
            break
        elif option == "2":
            client_socket.send(b"cadastrar")
            register(client_socket)
            break
        elif option == "3":
            client_socket.send(b"sair")
            response = client_socket.recv(1024).decode()
            print(response)
            break
        else:
            client_socket.send(b"invalido")
            response = client_socket.recv(1024).decode()
            print(response)
            print("Segue novamente as opções:")

    client_socket.close()

def authenticate(client_socket):
    #autenticacao por parte do cliente
    username = input("Digite o nome de usuário: ")
    client_socket.send(username.encode())
    password = input("Digite a senha: ")
    client_socket.send(password.encode())

    response = client_socket.recv(1024).decode()
    print(response)

    if response == "Autenticado com sucesso!":
        chat(client_socket)

    #.close() é utilizado para liberar recursos do sistema e informar ao cliente que a comunicação com o servidor foi encerrada
    client_socket.close()

def register(client_socket):
    new_username = input("Digite o nome de usuário desejado: ")
    client_socket.send(new_username.encode())
    new_password = input("Digite a senha desejada: ")
    client_socket.send(new_password.encode())
    response = client_socket.recv(1024).decode()
    print(response)
    if response == "Usuario ja existe!":
        register(client_socket)
    else:
        authenticate(client_socket)

def chat(client_socket):
    thread = threading.Thread(target=receive_messages, args=[client_socket], daemon=True)
    thread.start()

    print("'/exit' para sair ou '/p <destinatário> <mensagem>' para uma mensagem privada")
    while True:
        message = input()
        client_socket.sendall(message.encode())
        if message == "/exit":
            print("Você foi desconectado \n")
            break

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(message)
        except:
            break

#executar a main sempre após todas as funções estarem escritas acima
if __name__ == "__main__":
    main()