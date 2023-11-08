import threading
import logging

# Initialize the logging configuration
logging.basicConfig(filename='dme.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class DistributedLock:
    def __init__(self, num_clients):
        self.requested = [False] * num_clients
        self.timestamp = [0] * num_clients
        self.num_clients = num_clients
        self.lock = threading.Lock()

    def request_access(self, client_id):
        with self.lock:
            self.requested[client_id] = True
            self.timestamp[client_id] = max(self.timestamp) + 1
            logging.info(f'Client {client_id} requested access.')

    def release_access(self, client_id):
        with self.lock:
            self.requested[client_id] = False
            logging.info(f'Client {client_id} released access.')

    def can_access(self, client_id):
        with self.lock:
            for i in range(self.num_clients):
                if i != client_id and (
                    self.requested[i]
                    and (self.timestamp[i] < self.timestamp[client_id] or (self.timestamp[i] == self.timestamp[client_id] and i < client_id))
                ):
                    logging.info(f'Client {client_id} denied access.')
                    return False
            logging.info(f'Client {client_id} granted access.')
            return True
