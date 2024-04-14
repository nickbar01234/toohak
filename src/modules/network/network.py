import threading
import socket
import logging
from ..type.aliases import *
from ..serializable import serializer as s

logger = logging.getLogger(__name__)
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # socket access is not thread-safe between client's main thread and listener thread

    def connect(self, ip: str):
        logger.info("Connecting to %s", ip)
        host, port = ip.split(":")
        self.client.connect((host, int(port)))
        s.decode_connect_response(self.client.recv(2048))
        logger.info("Connection established.")

    def disconnect(self):
        self.client.close()

    def send_role(self, role: str):
        self.client.sendall(s.encode_role(role))
        # TODO: match on received response to handle errors?
        s.decode_role_response(self.client.recv(2048))
        logger.info("Player's role is updated on the server.")

    def send_name(self, name):
        self.client.sendall(s.encode_name(name))
        # TODO: match on received response to handle errors?
        s.decode_name_response(self.client.recv(2048))
        logger.info("Player's name is updated on the server.")

    def receive_questions(self) -> list[Question]:
        self.client.setblocking(True)
        questions = s.decode_questions(self.client.recv(100_000_000))
        logger.info("Received questions from the server: %s", str(questions))
        self.client.sendall(s.encode_ack("questions"))
        return questions

    def update_progress(self, progress: PlayerProgress):
        self.client.sendall(s.encode_progress(progress))
        logger.info("Player's updated progress is sent to the server")

    def receive_leadersboard(self) -> LeadersBoard:
        leadersboard = s.decode_leadersboard(self.client.recv(2048))
        logger.debug("Received leader's board from server: %s", leadersboard)
        return leadersboard

    def receive_leadersboard_or_game_ends(self) -> tuple[bool, LeadersBoard]:
        data = self.client.recv(2048)
        return s.decode_update_or_endgame(data)

    def block_until_game_starts(self):
        self.client.setblocking(True)
        logger.debug(
            "Blocking until received gamestart signal from the server.")
        initial_leadersboard = s.decode_startgame(self.client.recv(2048))
        logger.debug("Received game start signal.")
        self.client.sendall(s.encode_ack("game starts"))
        return initial_leadersboard

    def block_until_game_ends(self):
        self.client.setblocking(True)
        logger.debug(
            "Blocking until received gameends signal from the server.")
        s.decode_endgame(self.client.recv(2048))
        logger.debug("Received game ends signal.")

    def send_signal_start_game(self):
        self.client.sendall(s.encode_referee_startgame())
