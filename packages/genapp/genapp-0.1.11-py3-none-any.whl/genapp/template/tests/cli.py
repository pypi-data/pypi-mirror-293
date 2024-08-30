import socket


def send_http_request():
    # Crea un socket TCP/IP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Conecta el socket al servidor en el puerto dado
        client_socket.connect(('localhost', 8000))

        # Envía la solicitud HTTP CONNECT
        request = "CONNECT {}:{} HTTP/1.1\r\nHost: www.google.com\r\n\r\n".format(
            'localhost', 8000, 'localhost')
        client_socket.sendall(request.encode())

        # Lee la respuesta del servidor
        response = b''
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            response += data

        print("Respuesta del servidor:")
        print(response.decode())

    finally:
        # Cierra el socket
        client_socket.close()
