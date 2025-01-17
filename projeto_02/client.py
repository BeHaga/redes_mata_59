# TODO
#  - conexao com o servidor para implementar as funcionalidades e requisitos do projeto

# - cada cliente se comunica com o servidor, que gerenciara a comunicacao entre clientes
# - cada cliente deve se cadastrar junto ao servidor como um usuario
# - cada cliente deve poder se comunicar com outro cliente usando o nome de usuario (semelhante ao que ocorre no WhatsApp atraves do numero de telefone)
# - (OPCIONAL) clientes podem se juntar a grupos multicast (semelhante ao que ocorre no whatsapp)

import socket
import threading
from crypto import AES

aes = AES()

def main():
    #.AF_INET para comunicação baseada em IPs no formato protocolo IPv4
    #.SOCK_STREAM implementação de socket TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #esse IP é o padrão de loopback, utilizado em desenvolvimento local
    client_socket.connect(("127.0.0.1", 12345))
    client_socket.sendall(aes.key)
    
    print("Seja bem vindo! Escolha uma das opções a seguir: ")

    while True:
        print("1 - Autenticar")
        print("2 - Cadastrar novo usuário")
        print("3 - Sair")
        option = input("Digite o número da opção desejada: ")

        if option == "1":
            client_socket.send(aes.encrypt("autenticar"))
            authenticate(client_socket)
            break
        elif option == "2":
            client_socket.send(aes.encrypt("cadastrar"))
            register(client_socket)
            break
        elif option == "3":
            client_socket.send(aes.encrypt("sair"))
            response = aes.decrypt(client_socket.recv(1024))
            print(response)
            break
        else:
            client_socket.send(aes.encrypt("invalido"))
            response = aes.decrypt(client_socket.recv(1024))
            print(response)
            print("Segue novamente as opções:")

    client_socket.close()

def authenticate(client_socket):
    #autenticacao por parte do cliente
    username = input("Digite o nome de usuário: ")
    client_socket.send(aes.encrypt(username))
    password = input("Digite a senha: ")
    client_socket.send(aes.encrypt(password))

    response = aes.decrypt(client_socket.recv(1024))
    print(response)

    if response == "Autenticado com sucesso!":
        chat(client_socket)

    #.close() é utilizado para liberar recursos do sistema e informar ao cliente que a comunicação com o servidor foi encerrada
    client_socket.close()

def register(client_socket):
    new_username = input("Digite o nome de usuário desejado: ")
    client_socket.send(aes.encrypt(new_username))
    new_password = input("Digite a senha desejada: ")
    client_socket.send(aes.encrypt(new_password))
    response = aes.decrypt(client_socket.recv(1024))
    print(response)
    if response == "Usuario ja existe!":
        register(client_socket)
    else:
        authenticate(client_socket)

def chat(client_socket):
    thread = threading.Thread(target=receive_messages, args=[client_socket], daemon=True)
    thread.start()

    print("'/exit' para sair ou '/p <destinatário> <mensagem>' para uma mensagem privada ou '/file <destinatário> <caminho_do_arquivo> para um arquivo")
    while True:
        message = input()
        if message.startswith("/file"):
            _, receiver, file_path = message.split(" ", 2)
            send_file(client_socket, receiver, file_path)
        else:
            client_socket.sendall(aes.encrypt(message))
            if message == "/exit":
                print("Você foi desconectado \n")
                break

def receive_messages(client_socket):
    while True:
        try:
            message = aes.decrypt(client_socket.recv(1024))
            if message:
                print(message)
        except:
            break     

def send_file(client_socket, receiver, file_path):
    with open(file_path, "rb") as file:
        file_content = file.read()
    file_name = file_path.split("/")[-1]
    message = f"/file {receiver} {file_name} {len(file_content)}"
    client_socket.sendall(aes.encrypt(message))
    client_socket.sendall(file_content)
    print(f"Arquivo '{file_name}' enviado para {receiver}.")

#executar a main sempre após todas as funções estarem escritas acima
if __name__ == "__main__":
    main()