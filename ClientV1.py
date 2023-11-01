import socket

from kazoo.client import KazooClient

from dme_algorithm import DistributedLock



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

            print("Invalid command. Please use 'view', 'post <text>', or 'exit.")



if __name__ == '__main__':

    chat_file = "chat.txt"

    zk = KazooClient(hosts='172.31.13.196:2181', timeout=15.0)

    zk.start()

    dme_lock = DistributedLock(num_clients=3)  # Change the number of clients as needed

    user(zk, dme_lock)





