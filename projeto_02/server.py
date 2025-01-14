# TODO
#  - criar um servidor para implementar as funcionalidades e requisitos do projeto

import socket

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 12345))
    server_socket.listen(5)  # Aguarda até 5 conexões
    print("Servidor iniciado. Aguardando conexões...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Conexão estabelecida com {addr}")
        client_socket.send(b"Bem-vindo ao servidor!")
        client_socket.close()

if __name__ == "__main__":
    main()