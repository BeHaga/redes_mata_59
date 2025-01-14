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
    #1024 bytes é o tamanho máximo a ler por chamada do que vem no socket
    message = client_socket.recv(1024)
    #.decode() transforma de bytes para string
    print("Mensagem do servidor:", message.decode())
    #.close() é utilizado para liberar recursos do sistema e informar ao cliente que a comunicação com o servidor foi encerrada
    client_socket.close()

if __name__ == "__main__":
    main()

#é necessário solicitar ao cliente login e senha para fazer a autenticação e se manter conectado ao servidor graças ao thread