import socket

def send_message(url: str, host: str = '127.0.0.1', port: int = 65432) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        message = f"lynq://{url}"
        s.sendall(message.encode())

        data = s.recv(1024).decode()
        print('Received from server:', data)