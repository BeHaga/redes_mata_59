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