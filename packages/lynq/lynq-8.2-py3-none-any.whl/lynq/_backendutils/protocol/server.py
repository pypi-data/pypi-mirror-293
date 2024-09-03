import socket
import urllib.parse

def handle_client(connection: socket.socket) -> None:
    while True:
        data = connection.recv(1024).decode()
        if not data:
            break

        # Example: lynq://arg1=foo&arg2=bar
        if data.startswith("lynq://"):
            url = data[7:]  # Remove "lynq://"
            parsed_url = urllib.parse.urlparse(f"http://{url}")
            query_params = urllib.parse.parse_qs(parsed_url.query)

            # Process arguments
            response_message = "Processed arguments:\n"
            for key, values in query_params.items():
                response_message += f"{key}: {', '.join(values)}\n"

            connection.sendall(response_message.encode())
        else:
            connection.sendall(b"Invalid protocol")

def start_server(host: str = '127.0.0.1', port: int = 65432) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server listening on {host}:{port}")

        while True:
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                handle_client(conn)

if __name__ == "__main__":
    start_server()