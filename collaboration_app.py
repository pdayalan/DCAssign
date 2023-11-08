import socket
import time

chat_file = "chat.txt"

def serve(zk, dme_lock):
    host = '127.0.0.1'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(3)

    print("Server is listening...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        handle_client(client_socket, zk, dme_lock)

def handle_client(client_socket, zk, dme_lock):
    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            break
        if data == 'view':
            send_chat(client_socket)
        elif data.startswith('post'):
            post_message(data[5:], zk, dme_lock)
    client_socket.close()

def send_chat(client_socket):
    with open(chat_file, 'r') as chat_file:
        messages = chat_file.read()
    client_socket.send(messages.encode('utf-8'))

def post_message(message, zk, dme_lock):
    with dme_lock:
        with open(chat_file, 'a') as chat_file:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            chat_file.write(f"{timestamp} - User: {message}\n")
