import logging
import socket
import threading
import pickle
import sys
from modules import serializer as s
from modules.question.multiple_choice_question_builder import MultipleChoiceQuestionBuilder
from modules.solution.multiple_choice_solution_builder import MultipleChoiceSolutionBuilder


logger = logging.getLogger()
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

# Mock the set of questions TODO: remove once we have an actual set of questions
questions = [
    MultipleChoiceQuestionBuilder()
    .add_question("What's Tony's last name")
    .add_option("Doan")
    .add_option("Xu")
    .add_option("Huang")
    .add_option("Sheldon")
    .add_solution(MultipleChoiceSolutionBuilder().add_solution("Huang").build())
    .build(),
    MultipleChoiceQuestionBuilder()
    .add_question("What day is it")
    .add_option("Mon")
    .add_option("Tue")
    .add_option("Wed")
    .add_solution(MultipleChoiceSolutionBuilder().add_solution("Mon").build())
    .build()
]

type Name = str
type PlayerProgress = tuple[int, list[bool]]
type Address = str


class Server:
    def __init__(self, ip, port):
        # server info
        self.__addr = (ip, port)

        self.__referee_sockets_lock = threading.Lock()
        self.__referee_sockets = []

        # players states
        self.__playerCount = 0
        self.__playerCountLock = threading.Lock()

        self.__playerSockets: dict[socket.socket, tuple[str, Name]] = {}
        self.__playerSocketsLocks: dict[socket.socket, threading.Lock] = {}
        # TODO: don't think a Lock is needed since each listener thread is updating its own key-value pair
        self.__playerState: dict[Name, PlayerProgress] = {}
        self.__playerStateLock = threading.Lock()
        self.__playerListeners: list[threading.Thread] = []

        self.__top5players: list[tuple[Name, int]] = []
        self.__top5playersLock = threading.Lock()

        # game state / info
        self.__questions = questions  # TODO: change later to receive from the referee
        self.__gameStarts = threading.Semaphore(0)  # block at first
        self.__gameEnds = None  # will be initialized after the playerCount is finalized

        self.__player_state: dict[tuple[socket.socket,
                                        Address], tuple[Name, list[bool]]] = {}
        self.__player_state_lock = threading.Lock()

    #  Start the server and wait for client connection

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(self.__addr)
        server_socket.listen()
        logger.info("Server started, listening on %s:%s",
                    self.__addr[0], self.__addr[1])

        try:
            while True:
                client, addr = server_socket.accept()
                client.sendall(s.encode_connect_success())
                logger.info("New connection from %s, %s",
                            addr, self.__playerCount)

                player_listener = threading.Thread(
                    target=self.player_listener, args=(client, addr), daemon=True)
                self.__playerListeners.append(player_listener)
                player_listener.start()
        except KeyboardInterrupt:
            server_socket.close()
        # TODO: add a graceful way to terminate the server & wait for the player threads (I.e. exit while loop)?
        # for listener in self.__playerListeners:
        #     listener.join()

    def listener(self, client: socket.socket, addr):
        logger.info("Listening from %s", addr)
        # TODO(nickbar01234) - Handle referee or player
        self.player_listener(client, addr)

    # For each listener's thread to receive message form a specific player

    def player_listener(self, player_socket: socket.socket, player_addr):
        import time
        try:
            logger.info(
                "Listener thread started to listen from %s", player_addr)

            # finalize establishing connection by receiving player's name
            # may raise InvalidMessage exception
            player_name = s.decode_name(player_socket.recv(2048))
            player_socket.sendall(s.encode_name_response())
            logger.info("Player's name %s from %s", player_name, player_addr)

            player_socket.sendall(s.encode_questions(self.__questions))
            time.sleep(1)
            player_socket.sendall(s.encode_startgame())

            with self.__player_state_lock:
                self.__player_state[(player_socket, player_addr)] = (
                    player_name, [])

            # TODO(nickbar01234) - Block until signal
            while True:
                data = player_socket.recv(2048)
                if data == 0:
                    break
            # player_socket.sendall(s.encode_questions(self.__questions))
            # player_socket.sendall(s.encode_startgame())
            # # make the whole block atomic?
            # # with self.__playerCountLock:  # TODO: temporarily use this to guard the whole sec

            # #     self.__playerSockets[player_socket] = (
            # #         player_addr, player_name)
            # #     self.__playerSocketsLocks[player_socket] = threading.Lock()

            # #     # distribute questions as soon as each player joined
            # #     player_socket.sendall(s.encode_questions(self.__questions))
            # #     player_socket.sendall(s.encode_startgame())
            # #     # self.broadcast("Game starts", s.encode_startgame())

            # #     self.__playerCount += 1
            # # Hardcoding for now: start the game when 2 players joined
            # # TODO: move this to where it's appropriate (referee should start the game instead)
            # # if self.__playerCount == 1:  # TODONOW: change back to 2
            # #     logger.info("Game starts")
            # #     self.broadcast("Game starts", s.encode_startgame())

            # #     # unblock all threads to start game
            # #     self.__gameStarts.release(self.__playerCount)
            # #     # self.__gameEnds = threading.Barrier(self.__playerCount)

            # # self.__gameStarts.wait()
            # for _ in range(len(self.__questions)):
            #     progress = s.decode_progress(player_socket.recv(2048))
            #     logger.info("Receive %s from %s", progress, player_name)
                # with self.__playerStateLock:
                #     logger.debug("Acquired the player state lock")
                #     self.__playerState[player_name] = progress

                #     player_state_list = self.__playerState.items()
                #     logger.debug("player_state_list: %s", player_state_list)

                #     dict(sorted(player_state_list,
                #          key=lambda item: item[1][0], reverse=True))
                #     new_top5players = list(
                #         map(lambda x: x[0], player_state_list[:5]))
                #     logger.debug("new_top5players: %s", new_top5players)
                # logger.debug("Released the player state lock")

                #     with self.__top5playersLock:
                #         if new_top5players != self.__top5players:
                #             self.__top5players = new_top5players
                #             encoded = s.encode_leadersboard(self.__top5players)
                #             self.broadcast(self.__top5players, encoded)

            # while True:
            #     pass
            # player_socket.sendall(s.encode_name_response())

            # Update server's state
            # with self.__playerCountLock:
            #     self.__playerCount += 1

            # with self.__playerStateLock:
            #     self.__playerState[player_name] = []

            # # TODO: Distribution questions - do i need to wait for a signal from the referee?
            # player_socket.sendall(s.encode_questions(self.__questions))

            # # TODO: wait for start signal from the referee; For now, start the game once 2 players have joined
            # logger.info(
            #     f"Player {player_name, player_addr} is waiting for the game to start")
            # self.__gameStarts.wait()

            # # Handling player's status update & broadcast updated leader's board
            # logger.info(f"Waiting for update from Player {
            #             player_name, player_addr}")
            # # should receive exactly num_questions update
            # for i in range(len(self.__questions)):
            #     playerProgress = s.decode_progress(
            #         player_socket.recv(2048))  # may throw InvalidMessage
            #     logger.info(f"Receive from {player_name, player_addr}: {
            #                 playerProgress}")

            # # Players have finished all the questions
            # logger.info(
            #     f"Player {player_name, player_addr} has finished all the questions")

            # # Game ends
            # i = self.__gameEnds.wait()
            # if i == 0:  # only one player needs to broadcast a message & log
            #     self.broadcast("game ends", s.encode_le)
            #     logger.info(f"Game ends: all players finished")

            # # TODO: how long does the player stay connected here (auto exit timeout?)
            # player_socket.settimeout(120)  # auto log out after 2 min
            # s.decode_leave(player_socket.recv(1024))
            # logger.info(
            #     f"Player {player_name, player_addr} left. Listener threading exiting..")
        except Exception as _:
            with self.__player_state_lock:
                if (player_socket, player_addr) in self.__player_state:
                    logger.error("Lost the connection with %s",
                                 self.__player_state[(player_socket, player_addr)])

        finally:
            with self.__player_state_lock:
                logger.info("Disconnecting %s", self.__player_state[(
                    player_socket, player_addr)][0])
                del self.__player_state[(player_socket, player_addr)]
            player_socket.close()

    # Message protocol for the server to broadcast updates to players and referee
    def broadcast(self, summary, encoded_message):
        for player_socket, (player_addr, player_name) in self.__playerSockets.items():
            try:
                with self.__playerSocketsLocks[player_socket]:
                    player_socket.sendall(encoded_message)
                    logger.debug(f"Sent the broadcasted message to Player {
                                 player_name, player_addr}: {str(summary)}")
            except:
                logger.error(f"Failed to send to {player_name, player_addr}")


if __name__ == "__main__":
    IP = socket.gethostbyname(socket.gethostname())
    PORT = 5559
    Server(IP, PORT).start()
