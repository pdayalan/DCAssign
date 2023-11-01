import socket

import time

import logging



chat_file = "chat.txt"



def serve(zk, dme_lock):

    host = '172.31.13.196'  # Replace with the appropriate IP address

    port = 12345



    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((host, port))

    server_socket.listen(3)



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

    with zk, dme_lock:

        with open(chat_file, 'a') as chat_file:

            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            chat_file.write(f"{timestamp} - User: {message}\n")



def user(zk, dme_lock):

    while True:

        print("Commands: view, post <text>, exit")

        command = input("Enter a command: ")



        if command == 'view':

            with zk.get_lock(dme_lock):

                with open(chat_file, 'r') as chat_file:

                    messages = chat_file.read()

                print(messages)

        elif command.startswith('post'):

            with zk.get_lock(dme_lock):

                with open(chat_file, 'a') as chat_file:

                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

                    user_message = f"{timestamp} - User: {command[5:]}\n"

                    chat_file.write(user_message)

                    print(f"Posted: {user_message}")

        elif command == 'exit':

            break

        else:

            print("Invalid command. Please use 'view', 'post <text>', or 'exit'.")



if __name__ == '__main__':

    zk = None  # You need to set up ZooKeeper here

    dme_lock = None  # You need to initialize DistributedLock here

    user(zk, dme_lock)








