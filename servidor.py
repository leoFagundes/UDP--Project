import socket

def show_connected_clients(clients):
    if clients:
        print(f"|  {'Clientes conectados':^30}   |")
        print(f"| {'Client_IP':^15} | {'Client_PORT':^15} |")
        for client in clients:
            ip, port = client
            print(f"| {ip:^15} | {port:^15} |")
        print()
    else:
        print("Nenhum cliente conectado no momento.")

def handle_handshake(UDPServerSocket, address, connected_clients):
    handshakeAck = "Handshake ACK"
    UDPServerSocket.sendto(str.encode(handshakeAck), address)
    connected_clients.add(address)
    print(f"\nhandshake: Cliente {address} conectado.\n")

def handle_disconnect(UDPServerSocket, address, connected_clients):
    if address in connected_clients:
        connected_clients.remove(address)
        print(f"\ndisconnect: Cliente {address} desconectado.\n")
        show_connected_clients(list(connected_clients))

def handle_client_message(UDPServerSocket, message, address):
    client_ip, client_port = address
    clientIP = f"\nIP: {client_ip} | Port: {client_port}"
    clientMsg = f"Mensagem do Cliente: {message.decode()}"
    print(clientIP)
    print(clientMsg)
    
    if message.decode() == "AA":
        response = "Resposta correta!"
    else:
        response = "Resposta incorreta!"

    UDPServerSocket.sendto(str.encode(response), address)

def run_server(localIP, localPort, bufferSize):
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPServerSocket.bind((localIP, localPort))
    print("Servidor UDP ativo e ouvindo...\n")

    connected_clients = set()

    while True:
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]

        if address not in connected_clients:
            if message.decode() == "handshake":
                handle_handshake(UDPServerSocket, address, connected_clients)
                show_connected_clients(list(connected_clients))
            continue

        if message.decode() == "disconnect":
            handle_disconnect(UDPServerSocket, address, connected_clients)
            continue

        handle_client_message(UDPServerSocket, message, address)

if __name__ == "__main__":
    LOCAL_IP = "10.6.0.40"
    LOCAL_PORT = 20001
    BUFFER_SIZE = 1024

    run_server(LOCAL_IP, LOCAL_PORT, BUFFER_SIZE)
