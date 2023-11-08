import socket
import kazoo
from kazoo.client import KazooClient
from kazoo.recipe.lock import Lock
from dme_algorithm import DistributedLock
import time
import logging

chat_file = "chat.txt"

def serve(zk, dme_lock):
    host = '127.0.0.1'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(3)

    # Configure logging for both server and client activities
    logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logging.info("Server is listening...")

    while True:
        client_socket, addr = server_socket.accept()
        logging.info(f"Connection from {addr}")
        handle_client(client_socket, zk, dme_lock)

def handle_client(client_socket, zk, dme_lock):
    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            break
        if data == 'view':
            logging.info('User accessed view command')
            send_chat(client_socket)
        elif data.startswith('post'):
            logging.info('User accessed post command')
            post_message(data[5:], zk, dme_lock)
    client_socket.close()

def send_chat(client_socket):
    with open(chat_file, 'r') as chat_file:
        messages = chat_file.read()
    client_socket.send(messages.encode('utf-8'))

def post_message(message, zk, dme_lock):
    with zk.get_lock(dme_lock):
        with open(chat_file, 'a') as chat_file:
            timestamp = time.strftime("%d %b %I:%M%p")
            chat_file.write(f"{timestamp} {message}\n")
            logging.info(f"Posted message: {message}")

if __name__ == '__main__':
    zk = None  # You need to set up ZooKeeper here
    dme_lock = None  # You need to initialize DistributedLock here
    serve(zk, dme_lock)
