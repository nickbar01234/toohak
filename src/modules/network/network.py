import socket
import logging
import pickle
from ..serializable import serializer as s

logger = logging.getLogger(__name__)
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

# Thought: network only used by clients? since each client will have a network object and
# server will implement its own message passing protocol => since it keeps the list of clients in its own class

type Progress = list[bool]  # TODO: again global type file?


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setblocking(True)

    def connect(self, ip: str):
        logger.info("Connecting to %s", ip)
        host, port = ip.split(":")
        self.client.connect((host, int(port)))

        # may raise InvalidMessage / timeout exception
        s.decode_connect_response(self.client.recv(2048))
        logger.info("Connection established.")

    def disconnect(self):
        self.client.close()

    def send_name(self, name):
        self.client.sendall(s.encode_name(name))
        # may raise InvalidMessage / timeout exception
        s.decode_name_response(self.client.recv(2048))
        logger.info("Player's name is updated on the server.")

    def receive_questions(self):
        # may raise InvalidMessage exception
        data = self.client.recv(100_000_000)
        logger.info("Received %s", pickle.loads(data))
        questions = s.decode_questions(data)
        return questions

    def update_progress(self, progress: Progress):
        self.client.sendall(s.encode_progress(progress))
        logger.info("Player's updated progress is sent to the server")

    def update_leaderboard(self, top5players):
        return

    def finish_game(self, time):
        return

    def receive_leadersboard(self):
        leadersboard = s.decode_leadersboard(self.client.recv(2048))
        logger.debug("Received leader's board from server: %s", leadersboard)
        return leadersboard

    def receive_leadersboard_or_game_ends(self):
        return s.decode_update_or_endgame(self.client.recv(2048))

    def receive_game_start(self):
        return s.decode_startgame(self.client.recv(2048))
