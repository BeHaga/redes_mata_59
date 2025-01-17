# TODO
#  - conexao com o servidor para implementar as funcionalidades e requisitos do projeto

# - cada cliente se comunica com o servidor, que gerenciara a comunicacao entre clientes
# - cada cliente deve se cadastrar junto ao servidor como um usuario
# - cada cliente deve poder se comunicar com outro cliente usando o nome de usuario (semelhante ao que ocorre no WhatsApp atraves do numero de telefone)
# - (OPCIONAL) clientes podem se juntar a grupos multicast (semelhante ao que ocorre no whatsapp)

import socket

def main():
    #.AF_INET para comunicação baseada em IPs no formato protocolo IPv4
    #.SOCK_STREAM implementação de socket TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #esse IP é o padrão de loopback, utilizado em desenvolvimento local
    client_socket.connect(("127.0.0.1", 12345))

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

def chat(client_socket):
    while True:
        message = input("Digite 'sair' para sair ou Digite sua mensagem: ")
        client_socket.send(message.encode())
        response = client_socket.recv(1024).decode()
        if response == "":
            print(f"Desconectado do servidor")
            return False
        print(f"Resposta do servidor: {response}")

#executar a main sempre após todas as funções estarem escritas acima
if __name__ == "__main__":
    main()