import logging
import socket
import threading
import sys
from modules import serializer as s
from modules.question.multiple_choice_question_builder import MultipleChoiceQuestionBuilder
from modules.solution.multiple_choice_solution_builder import MultipleChoiceSolutionBuilder


logger = logging.getLogger()
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

# Mock the set of questions TODO: remove once we have an actual set of questions
questions = [
    MultipleChoiceQuestionBuilder()
    .add_question("What's Tony's last name ----")
    .add_option("Doan")
    .add_option("Xu")
    .add_option("Huang")
    .add_solution(MultipleChoiceSolutionBuilder().add_solution("Huang").build())
    .build()
    ]

type Name = str 
type PlayerProgress = tuple[int, list[bool]]
type Address = str

class Server:
    def __init__(self, ip, port):
        # server info
        self.__addr = (ip, port)

        # players states
        self.__playerCount = 0
        self.__playerCountLock = threading.Lock()

        self.__playerSockets: dict[socket.socket, tuple[str, Name]] = {} 
        self.__playerSocketsLocks: dict[socket.socket, threading.Lock] = {}
        self.__playerState: dict[Name, PlayerProgress] = {}  # TODO: don't think a Lock is needed since each listener thread is updating its own key-value pair
        self.__playerStateLock = threading.Lock()
        self.__playerListeners : list[threading.Thread] = []

        self.__top5players: list[tuple[Name, int]] = []
        self.__top5playersLock = threading.Lock()

        # game state / info
        self.__questions = questions # TODO: change later to receive from the referee
        self.__gameStarts = threading.Semaphore(0) # block at first
        self.__gameEnds = None # will be initialized after the playerCount is finalized

    #  Start the server and wait for client connection
    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(self.__addr)
        server_socket.listen()
        logger.info("Server started, listening on %s:%s",
                    self.__addr[0], self.__addr[1])

        while True:
            player_socket, player_addr = server_socket.accept()
            player_socket.sendall(s.encode_connect_success())
            logger.info(f"New connection from {player_addr}, {self.__playerCount}")

            player_listener = threading.Thread(
                target=self.player_listener, args=(player_socket, player_addr))
            self.__playerListeners.append(player_listener)
            player_listener.start()

            # TODO: move the code & change this conditional later to listen from the referee
            with self.__playerCountLock:
                if self.__playerCount == 2: # WARNING: currently the game only allows for 2 players
                    self.__gameStarts.release(self.__playerCount) # unblock all threads to start game
                    self.__gameEnds = threading.Barrier(self.__playerCount)

                    # broadcasting to let the clients know game starts 
                    self.broadcast("game starts", s.encode_startgame)

                    for listener in self.__playerListeners:
                        listener.join()
                    break 

        # TODO: add a graceful way to terminate the server 
        


    # For each listener's thread to receive message form a specific player
    def player_listener(self, player_socket, player_addr):
        try:
            logger.info(
                f"Listener thread started to listen from {player_addr}")
            # finalize establishing connection
            player_name = s.decode_name(player_socket.recv(2048)) # may raise InvalidMessage exception
            logger.info(f"Player's name from {player_name, player_addr} is {player_name}")
            self.__playerSockets[player_socket] = (player_addr, player_name)
            self.__playerSocketsLocks[player_socket] = threading.Lock() # TODO: with line above -> make it atomic?

            with self.__playerCountLock:
                self.__playerCount += 1

            with self.__playerStateLock:
                self.__playerState[player_name] = []
            
            player_socket.sendall(s.encode_name_response())

            # TODO: Distribution questions - do i need to wait for a signal from the referee?
            player_socket.sendall(s.encode_questions(self.__questions))

            # TODO: wait for start signal from the referee; For now, start the game once 2 players have joined 
            logger.info(f"Player {player_name, player_addr} is waiting for the game to start")
            self.__gameStarts.wait()
            
            # Handling player's status update & broadcast updated leader's board
            logger.info(f"Waiting for update from Player {player_name, player_addr}")
            for i in range(len(self.__questions)): # should receive exactly num_questions update
                playerProgress = s.decode_progress(player_socket.recv(2048)) # may throw InvalidMessage
                logger.info(f"Receive from {player_name, player_addr}: {playerProgress}")
                with self.__playerStateLock:
                    self.__playerState[player_name] = playerProgress
                    playerStateList = self.__playerState.items()
                    dict(sorted(playerStateList, key = lambda item: item[1][0], reverse=True))
                    new_top5players = list(map(lambda x: x[0], playerStateList[:5]))
                
                    with self.__top5playersLock:
                        if new_top5players != self.__top5players:   
                            self.__top5players = new_top5players
                            encoded = s.encode_leadersboard(self.__top5players)
                            self.broadcast(self.__top5players, encoded)
                
            # Players have finished all the questions 
            logger.info(f"Player {player_name, player_addr} has finished all the questions")

            # Game ends
            i = self.__gameEnds.wait()
            if i == 0: # only one player needs to broadcast a message & log
                self.broadcast("game ends", s.encode_le)
                logger.info(f"Game ends: all players finished")
            
            # TODO: how long does the player stay connected here (auto exit timeout?)
            player_socket.settimeout(120) # auto log out after 2 min
            s.decode_leave(player_socket.recv(1024))
            logger.info(f"Player {player_name, player_addr} left. Listener threading exiting..")

        except:
            logger.error(f"Lost the connection with {player_name, player_addr}")
        
        finally:
            if player_socket in self.__playerSockets:
                with self.__playerSocketsLocks[player_socket]:
                    del self.__playerSockets[player_socket]
            player_socket.close()

    # Message protocol for the server to broadcast updates to players and referee
    def broadcast(self, summary, encoded_message):
        for player_socket, (player_addr, player_name) in self.__playerSockets.items():
            try:
                with self.__playerSocketsLocks[player_socket]:
                    player_socket.sendall(encoded_message)
                    logger.debug(f"Sent the broadcasted message to Player {player_name, player_addr}: {str(summary)}")
            except:
                logger.error(f"Failed to send to {player_name, player_addr}")


if __name__ == "__main__":
    IP = socket.gethostbyname(socket.gethostname())
    PORT = 5555
    Server(IP, PORT).start()
