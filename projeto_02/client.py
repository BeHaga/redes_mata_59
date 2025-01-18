# TODO
#  - conexao com o servidor para implementar as funcionalidades e requisitos do projeto

# - cada cliente se comunica com o servidor, que gerenciara a comunicacao entre clientes
# - cada cliente deve se cadastrar junto ao servidor como um usuario
# - cada cliente deve poder se comunicar com outro cliente usando o nome de usuario (semelhante ao que ocorre no WhatsApp atraves do numero de telefone)
# - (OPCIONAL) clientes podem se juntar a grupos multicast (semelhante ao que ocorre no whatsapp)

import socket
import threading
from crypto import AES
from time import sleep

aes = AES()

def main():
    global exitFlag
    exitFlag = False

    global client_socket
    #.AF_INET para comunicação baseada em IPs no formato protocolo IPv4
    #.SOCK_STREAM implementação de socket TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #esse IP é o padrão de loopback, utilizado em desenvolvimento local
    client_socket.connect(("127.0.0.1", 12345))
    client_socket.sendall(aes.key)
    connected = True
    
    print("Seja bem vindo! Escolha uma das opções a seguir: ")

    while connected:
        try:
            print("1 - Autenticar")
            print("2 - Cadastrar novo usuário")
            print("3 - Sair")
            option = input("Digite o número da opção desejada: ")

            if option == "1":
                client_socket.sendall(aes.encrypt("autenticar"))
                if authenticate():
                    continue
                break
            elif option == "2":
                client_socket.sendall(aes.encrypt("cadastrar"))
                if register():
                    continue
                break
            elif option == "3":
                client_socket.sendall(aes.encrypt("sair"))
                response = aes.decrypt(client_socket.recv(1024))
                print(response)
                break
            else:
                client_socket.sendall(aes.encrypt("invalido"))
                response = aes.decrypt(client_socket.recv(1024))
                print(response)
                print("Segue novamente as opções:")
        except socket.error:
            connected = handle_disconnection()

    client_socket.close()

def authenticate():
    global client_socket
    try:
        #autenticacao por parte do cliente
        username = input("Digite o nome de usuário: ")
        client_socket.sendall(aes.encrypt(username))
        password = input("Digite a senha: ")
        client_socket.sendall(aes.encrypt(password))

        response = aes.decrypt(client_socket.recv(1024))
        print(response)

        if response == "Autenticado com sucesso!":
            if chat():
                return True

        #.close() é utilizado para liberar recursos do sistema e informar ao cliente que a comunicação com o servidor foi encerrada
        client_socket.close()
    except socket.error:
        connected = handle_disconnection()
        if connected:
            return True

def register():
    global client_socket
    try:
        new_username = input("Digite o nome de usuário desejado: ")
        client_socket.sendall(aes.encrypt(new_username))
        new_password = input("Digite a senha desejada: ")
        client_socket.sendall(aes.encrypt(new_password))
        response = aes.decrypt(client_socket.recv(1024))
        print(response)
        if response == "Usuario ja existe!":
            return True
        else:
            if authenticate():
                return True
    except socket.error:
        connected = handle_disconnection()
        if connected:
            return True

def chat():
    global client_socket
    global exitFlag
    global reconnectFlag
    exitFlag = False
    reconnectFlag = False
    thread = threading.Thread(target=receive_messages, daemon=True)
    thread.start()
    
    print("'/exit' para sair ou '/p <destinatário> <mensagem>' para uma mensagem privada ou '/file <destinatário> <caminho_do_arquivo> para um arquivo")
    while True:
        try:
            message = input()
            if reconnectFlag:
                thread.join()
                return True
            if message.startswith("/file"):
                _, receiver, file_path = message.split(" ", 2)
                send_file(receiver, file_path)
            elif message == "/exit":
                exitFlag = True
                client_socket.sendall(aes.encrypt(message))
                client_socket.close()
                thread.join()
                print("Você foi desconectado \n")
                return False
            else:
                client_socket.sendall(aes.encrypt(message))
        except socket.error:
            connected = handle_disconnection()
            return connected

def receive_messages():
    global client_socket
    global exitFlag
    global reconnectFlag
    while not exitFlag:
        try:
            encrypted_message = client_socket.recv(1024)
            message = aes.decrypt(encrypted_message)
            if message:
                print(message)
        except socket.error:
            if not exitFlag:
                if handle_disconnection():
                    print("Envie qualquer caractere para retomar a aplicação")
                    reconnectFlag = True
                    return

def send_file(receiver, file_path):
    global client_socket
    with open(file_path, "rb") as file:
        file_content = file.read()
    file_name = file_path.split("/")[-1]
    message = f"/file {receiver} {file_name} {len(file_content)}"
    client_socket.sendall(aes.encrypt(message))
    client_socket.sendall(file_content)
    print(f"Arquivo '{file_name}' enviado para {receiver}.")

def handle_disconnection():
    global client_socket
    global exitFlag
    if not exitFlag:
        connected = False
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #recria socket para reconexão
        print("Conexão perdida! Reconectando...")
        attempts = 0
        while not connected:
            if attempts >= 5: #Após 15 segundos tentando reconexão
                print("Não foi possível se conectar ao servidor. Encerrando aplicação...")
                return connected
            try:
                client_socket.connect(("127.0.0.1", 12345))
                client_socket.sendall(aes.key)
                connected = True
                print("Reconectado!")
                return connected
            except socket.error:
                sleep(3)
                attempts += 1

#executar a main sempre após todas as funções estarem escritas acima
if __name__ == "__main__":
    main()