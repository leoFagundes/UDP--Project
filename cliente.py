import socket

def send_handshake(UDPClientSocket: socket.socket, serverAddressPort: tuple, bufferSize: int) -> bool:
    """
    Envia uma mensagem de handshake para o servidor e aguarda a confirmação.

    Args:
        UDPClientSocket (socket.socket): Socket do cliente UDP.
        serverAddressPort (tuple): Tupla contendo endereço IP e porta do servidor.
        bufferSize (int): Tamanho do buffer para recebimento de mensagens.

    Returns:
        bool: True se o handshake for bem-sucedido, False caso contrário.
    """
    handshake_message = "handshake"
    UDPClientSocket.sendto(str.encode(handshake_message), serverAddressPort)
    msgFromServer, _ = UDPClientSocket.recvfrom(bufferSize)
    return msgFromServer.decode() == "Handshake ACK"

def send_message(UDPClientSocket: socket.socket, serverAddressPort: tuple, message: str, bufferSize: int) -> str:
    """
    Envia uma mensagem para o servidor e aguarda a resposta.

    Args:
        UDPClientSocket (socket.socket): Socket do cliente UDP.
        serverAddressPort (tuple): Tupla contendo endereço IP e porta do servidor.
        message (str): Mensagem a ser enviada para o servidor.
        bufferSize (int): Tamanho do buffer para recebimento de mensagens.

    Returns:
        str: Resposta recebida do servidor.
    """
    UDPClientSocket.sendto(str.encode(message), serverAddressPort)
    msgFromServer, _ = UDPClientSocket.recvfrom(bufferSize)
    return msgFromServer.decode()

def send_disconnect(UDPClientSocket: socket.socket, serverAddressPort: tuple, bufferSize: int) -> None:
    """
    Envia uma mensagem de desconexão para o servidor.

    Args:
        UDPClientSocket (socket.socket): Socket do cliente UDP.
        serverAddressPort (tuple): Tupla contendo endereço IP e porta do servidor.
        bufferSize (int): Tamanho do buffer para recebimento de mensagens.
    """
    disconnect_message = "disconnect"
    UDPClientSocket.sendto(str.encode(disconnect_message), serverAddressPort)

def run_client(serverAddressPort: tuple, bufferSize: int) -> None:
    """
    Executa o cliente UDP, estabelece conexão com o servidor e permite o envio de mensagens.

    Args:
        serverAddressPort (tuple): Tupla contendo endereço IP e porta do servidor.
        bufferSize (int): Tamanho do buffer para recebimento de mensagens.
    """
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    if send_handshake(UDPClientSocket, serverAddressPort, bufferSize):
        print("Conexão estabelecida com o servidor.\n")

        try:
            while True:
                user_input = input("Digite uma mensagem ('sair' para encerrar): ")
                if user_input.lower() == "sair":
                    break
                response = send_message(UDPClientSocket, serverAddressPort, user_input, bufferSize)
                print(f"Mensagem do Servidor: {response}\n")
        finally:
            send_disconnect(UDPClientSocket, serverAddressPort, bufferSize)
            print("Desconectado do servidor.")

    else:
        print("Falha ao estabelecer conexão com o servidor.")

    UDPClientSocket.close()

if __name__ == "__main__":
    SERVER_ADDRESS_PORT = ("10.6.0.40", 20001)
    BUFFER_SIZE = 1024

    run_client(SERVER_ADDRESS_PORT, BUFFER_SIZE)
