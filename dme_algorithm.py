import threading



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



    def release_access(self, client_id):

        with self.lock:

            self.requested[client_id] = False



    def can_access(self, client_id):

        with self.lock:

            for i in range(self.num_clients):

                if i != client_id and (

                    self.requested[i]

                    and (self.timestamp[i] < self.timestamp[client_id] or (self.timestamp[i] == self.timestamp[client_id] and i < client_id))

                ):

                    return False

            return True



