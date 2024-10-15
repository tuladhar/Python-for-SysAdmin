import socket

# Check if a server is up
def check_server(host, port):
    try:
        with socket.create_connection((host, port), timeout=5):
            print(f"{host}:{port} is up")
    except socket.error:
        print(f"{host}:{port} is down")

# Example usage
check_server("google.com", 80)
