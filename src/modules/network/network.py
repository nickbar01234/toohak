import socket 
import serializable as s

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

# Thought: network only used by clients? since each client will have a network object and 
# server will implement its own message passing protocol => since it keeps the list of clients in its own class

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(5.0) # may raise socket.timeout exception
        self.server = "10.0.0.137" # WARNING: hardcode & need to be consistenet with server.py
        self.port = 5555
        self.server_addr = (self.server, self.port)
        self.connect()
    
    def connect(self):
        try: 
            self.client.connect(self.server_addr)
            if s.decode_connect_response(self.client.recv(2048)):
                logger.info("Connection established.")
            else:
                logger.error("Connection failed to establish.")
        except:
            pass 
    
    def send_name(self, name):
        try:
            self.client.send(s.encode_name(name))
            if s.decode_name_response(self.client.recv(2048)):
                logger.info("Player's name is updated on the server.")
            else:
                logger.error("Player's name is not correctly updated on the server.")
        except socket.error as e:
            print(e)
    
    def send_questions(questions):
        return
    def update_progress(name, ans):
        return
    def update_leaderboard(top5players):
        return
    def finish_game(time):
        return

# Testing 
n = Network()
print(n.send_name("Toffoli"))