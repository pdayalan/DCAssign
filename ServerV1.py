import socket
import kazoo
from kazoo.client import KazooClient
from collaboration_app import serve
from dme_algorithm import DistributedLock

zk = KazooClient(hosts='172.31.13.196:2181', timeout=15.0)
zk.start()

dme_lock = DistributedLock(num_clients=3)  # Change the number of clients as needed

serve(zk, dme_lock)
