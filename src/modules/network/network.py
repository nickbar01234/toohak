import socket
from ..serializable import serializer as s

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

# Thought: network only used by clients? since each client will have a network object and
# server will implement its own message passing protocol => since it keeps the list of clients in its own class


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, ip: str):
        logger.info("Connecting to %s", ip)
        host, port = ip.split(":")
        self.client.connect((host, int(port)))

        s.decode_connect_response(self.client.recv(2048)) # may raise InvalidMessage / timeout exception
        logger.info("Connection established.")

    def send_name(self, name):
        self.client.send(s.encode_name(name))
        s.decode_name_response(self.client.recv(2048)) # may raise InvalidMessage / timeout exception
        logger.info("Player's name is updated on the server.")

    def receive_questions(self):
        self.client.setblocking(True) # block until get the questions
        questions = s.decode_questions(self.client.recv(4096)) # may raise InvalidMessage exception 
        return questions

    def update_progress(self, name, ans):
        return

    def update_leaderboard(self, top5players):
        return

    def finish_game(self, time):
        return

    def receive_leadersboard(self):
        leadersboard = s.decode_leadersboard(self.client.recv(2048))
        logger.debug(f"Received leader's board from server: {str(leadersboard)}")
        return leadersboard

    def receive_leadersboard_or_game_ends(self):
        self.client.setblocking(True)
        return s.decode_update_or_endgame(self.client.recv(2048))
