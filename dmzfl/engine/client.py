"""Client (vehicle). May be an attacker; exposes off-chain w_local + on-chain tx."""
from .worker import Worker
class Client(Worker):
    category = 'honest'