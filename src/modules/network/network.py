import threading
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
        # socket access is not thread-safe between client's main thread and listener thread
        self._lock = threading.Lock()

    def connect(self, ip: str):
        logger.info("Connecting to %s", ip)
        host, port = ip.split(":")
        self.client.connect((host, int(port)))
        s.decode_connect_response(self.client.recv(2048))
        logger.info("Connection established.")

    def disconnect(self):
        self.client.close()

    def send_name(self, name):
        self.client.sendall(s.encode_name(name))
        s.decode_name_response(self.client.recv(2048))
        logger.info("Player's name is updated on the server.")

    def receive_questions(self):
        self.client.setblocking(True)
        questions = s.decode_questions(self.client.recv(100_000_000))
        logger.info("Received questions from the server: %s", questions)
        return questions

    def update_progress(self, progress: Progress):
        self.client.sendall(s.encode_progress(progress))
        logger.info("Player's updated progress is sent to the server")

    def receive_leadersboard(self):
        leadersboard = s.decode_leadersboard(self.client.recv(2048))
        logger.debug("Received leader's board from server: %s", leadersboard)
        return leadersboard

    def receive_leadersboard_or_game_ends(self):
        return s.decode_update_or_endgame(self.client.recv(2048))

    def block_until_game_starts(self):
        self.client.setblocking(True)
        logger.debug(
            "Blocking until received gamestart signal from the server.")
        s.decode_startgame(self.client.recv(2048))
        logger.debug("Received game start signal.")
