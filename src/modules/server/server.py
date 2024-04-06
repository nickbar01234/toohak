import socket
import threading
import sys
from ..serializable import serializer as s

import logging
# logging.basicConfig(level=logging.WARNING)  # default logging level
logger = logging.getLogger()
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
# logger.setLevel(logging.DEBUG)

class ConnectionError(Exception):
    pass

class Server:
    def __init__(self, ip, port):
        self.addr = (ip, port)
        self.playerCount = 0
        self.playerSockets = {}  # {socket: (addr, name)}
        self.playerState = {}
        self.playerLocks = {}
        self.questions = []
        self.top5players = []
        self.top5playersLock = threading.Lock()
    
    #  Start the server and wait for client connection
    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(self.addr)
        server_socket.listen() 
        logger.info(f"Server started, listening on localhost:{port}")

        while True:
            player_socket, player_addr = server_socket.accept()
            player_socket.send(s.encode_connect_success())
            logger.info(f"New connection from {player_addr}, {self.playerCount}")

            player_listener = threading.Thread(target=self.player_listener, args=(player_socket, player_addr))
            player_listener.start()
    
    # For each listener's thread to receive message form a specific player
    def player_listener(self, player_socket, player_addr):
        try:
            logger.info(f"Listener thread started to listen from {player_addr}")
            # finalize establishing connection
            player_socket.settimeout(5.0)
            player_name = s.decode_name(player_socket.recv(2048))
            if not player_name:
                logger.error(f"{player_addr} failed to send the player's name.")
                raise ConnectionError
            logger.info(f"Player's name from {player_addr} is {player_name}")
            self.playerSockets[player_socket] = (player_addr, player_name)
            self.playerCount += 1
            player_socket.send(s.encode_name_response())
            
            logger.debug("REACHE HERE -> the rest feel free to ignore for now ") # TODO below
            # TODO: Distribution questions
            # TODO: Handling player's status update
            while True:
                data = player_socket.recv(2048)
                if not data:
                    break
                logger.info(f"Receive: {data}") # binary
                # TODO: some processing to update the state and compute top5
                self.update_leaderboard()
        except:
            logger.error(f"Lost the connection with {player_addr}")
        finally:
            if player_socket in self.playerSockets:
                del self.playerSockets[player_socket]
            player_socket.close()
    
    # Message protocol for the server to send updates of leaders board to players and referee
    def update_leaderboard(self):
        message = pickle.dumps(self.top5players)
        for player_socket, (player_addr, player_name) in self.playerSockets.items():
            try:
                player_socket.sendall(message)
            except:
                sys.stderr(f"Failed to send to {player_addr}")


# Testing establishing the connection
# WARNING: hardcode
server_ip = "10.0.0.137"
# server = "10.243.75.99"
port = 5555
Server(server_ip, port).start()