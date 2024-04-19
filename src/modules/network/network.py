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

        # for referee's senders when trying to send questions at around the same time
        self.client_lock = threading.Lock()

    def connect(self, ip: str):
        logger.info("Connecting to %s", ip)
        host, port = ip.split(":")
        self.client.connect((host, int(port)))
        s.decode_connect_response(self.client.recv(2048))
        logger.info("Connection established.")

    def disconnect(self):
        self.client.sendall(s.encode_quit())
        self.client.close()

    def send_role(self, role: str):
        self.client.sendall(s.encode_role(role))
        logger.debug("Waiting on role response")
        status = s.decode_role_response(self.client.recv(2048))
        logger.info(f"Client's role is {status} on the server.")
        return status

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

    def send_signal_start_game(self):
        self.client.sendall(s.encode_referee_startgame())

    #
    # Referee Protocols
    #

    def choose_default_or_customized(self, idx: int):
        self.client.sendall(s.encode_defaults_or_define_questions(idx))
        self.client.settimeout(5)
        s.decode_ack(self.client.recv(1024))
        logger.info(
            "Sent to server choosing questions set (-1 meaning self-defined): %d", idx)

    def send_question(self, question: Question):
        with self.client_lock:
            logger.debug("Sending question")
            self.client.sendall(s.encode_question(question))
            self.client.settimeout(10)
            s.decode_ack(self.client.recv(1024))
            logger.info("Question sent to the server: %s", question)

    def send_confirm(self):
        self.client.sendall(s.encode_confirm_questions())
        self.client.settimeout(5)
        s.decode_ack(self.client.recv(1024))
        logger.info("Question Confirmation sent to the server")

    def send_elapsed_time(self, seconds: int):
        self.client.sendall(s.encode_elapse_time(seconds))
