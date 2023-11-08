import socket
import kazoo
from kazoo.client import KazooClient
from kazoo.recipe.lock import Lock
from dme_algorithm import DistributedLock
import time
import logging

# Initialize the logging configuration
logging.basicConfig(filename='client_activity.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

chat_file = "/chat_file"  # Path to the shared chat file in ZooKeeper

def user(zk, dme_lock, machine_id):
    while True:
        print("Commands: view, post <text>, exit")
        command = input("Enter a command: ")

        if command == 'view':
            with Lock(zk, "/mylockpath"):
                messages = zk.get(chat_file)[0].decode('utf-8')
                print(messages)
                # Log the view command
                logging.info(f"{machine_id} - View command executed")

        elif command.startswith('post'):
            with Lock(zk, "/mylockpath"):
                timestamp = time.strftime("%d %b %I:%M%p")
                user_message = f"{timestamp} {machine_id}: {command[5:]}\n"
                current_messages = zk.get(chat_file)[0].decode('utf-8')
                updated_messages = current_messages + user_message
                zk.set(chat_file, bytes(updated_messages, 'utf-8'))
                print(f"Posted: {user_message}")
                # Log the posted message
                logging.info(f"{machine_id} - Posted message: {user_message}")

        elif command == 'exit':
            break

        else:
            print("Invalid command. Please use 'view', 'post <text>', or 'exit.")

if __name__ == '__main__':
    zk = KazooClient(hosts='172.31.13.196:2181', timeout=15.0)
    zk.start()
    dme_lock = DistributedLock(num_clients=3)
    machine_id = "Node2"  # Replace with a unique machine ID
    user(zk, dme_lock, machine_id)
