import logging
import socket
import threading
from modules import serializer as s
from modules import ServerState
from modules.type.aliases import *
from modules.state.question_set import NUM_QUESTIONS

logger = logging.getLogger()
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)


class Server:
    def __init__(self, ip, port):
        self.__state = ServerState(ip, port)

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_addr = self.__state.get_server_addr()
        server_socket.bind(server_addr)
        server_socket.listen()
        logger.info("Server started, listening on %s:%s",
                    server_addr[0], server_addr[1])

        game_starter_thread = threading.Thread(
            target=self.game_starter_thread, args=[], daemon=True)
        game_starter_thread.start()

        try:
            while True:
                client, addr = server_socket.accept()
                listener = threading.Thread(
                    target=self.listener, args=(client, addr), daemon=True)
                self.__state.add_listener(listener)
                listener.start()

        except KeyboardInterrupt:
            server_socket.close()
        # TODO: add a graceful way to terminate the server & wait for the player threads (I.e. exit while loop)?
        # for listener in self.__playerListeners:
        #     listener.join()

    # TODO: tell referee to quit when game ends
    def game_starter_thread(self):
        # TODO(nickbar01234) - Restart game thread to play another round?
        logger.info("Thread started to monitor the game_starting state.")

        self.__state.wait_game_start()
        logger.info("Game started")

        self.broadcast_with_ack("distribute questions", s.encode_questions(
            self.__state.get_questions()))

        # Broadcast to all players that the game has started TODO: how do we make sure all player threads have unblocked at this point?
        self.__state.init_leadersboard()
        init_top5players = self.__state.get_top5()
        self.broadcast_with_ack(
            "game starts", s.encode_startgame(init_top5players))

        # Send initialized full leadersboard to referee
        self.send_full_leadersboard()

        for address in self.__state.get_all_socket_addr():
            self.__state.player_signal_start_game(address)

        self.__state.wait_end()
        self.broadcast_without_ack("Broadcasting final results", s.encode_endgame(
            self.__state.get_final_results()))

    def listener(self, client: socket.socket, addr):
        logger.info("Listening from %s", addr)
        client.sendall(s.encode_connect_success())
        logger.info("Reciving role")
        role_selection = s.decode_role(client.recv(2048))
        recv_status = "success"

        with self.__state.referee_lock:
            if role_selection == "referee":
                # if another client is referee already
                if self.__state.get_referee():
                    recv_status = "failure"
                    role_selection = "player"
                else:
                    self.__state.set_referee((client, addr))

        client.sendall(s.encode_role_response(recv_status))
        match role_selection:
            case "player":
                return self.player_listener(client, addr)
            case "referee":
                return self.referee_listener(client, addr)

    # For each listener's thread to receive message form a specific player

    def player_listener(self, player_socket: Socket, player_addr: Addr):
        try:
            socket_addr = (player_socket, player_addr)
            player_lock = threading.Lock()
            logger.info(
                "Listener thread started to listen from %s", player_addr)

            # finalize establishing connection by receiving player's name
            player_name = self.receive_player_name(player_socket, player_lock)
            self.__state.add_player(
                player_socket, player_addr, player_name, player_lock)

            # Wait for game starts
            self.__state.player_wait_start_game(socket_addr)

            for _ in range(len(self.__state.get_questions())):
                logger.debug(
                    "Waiting to receive update from the player %s", player_name)
                progress = s.decode_progress(player_socket.recv(2048))
                logger.info("Receive %s from %s", progress, player_name)
                self.__state.update_player_progress(socket_addr, progress)
                # if (top5 := self.__state.update_top5()):
                if (top5 := self.__state.get_top5()):
                    logger.debug("Sending updated top 5")
                    self.broadcast_without_ack(
                        "new top5", s.encode_leadersboard(top5))
                self.send_full_leadersboard()

            elapsed_time = s.decode_elapse_time(player_socket.recv(1024))
            self.__state.update_end_results(socket_addr, elapsed_time)
            self.__state.signal_end()

            _quit = s.decode_quit(player_socket.recv(1024))
        finally:
            logger.info("Removing %s", socket_addr)
            self.__state.remove_player(socket_addr)

    def referee_listener(self, referee_socket: socket.socket, referee_addr):
        socket_addr = (referee_socket, referee_addr)
        try:
            logger.info(
                "Referee thread started to listen from %s", referee_addr)

            # TODO: Add a scene to use the default question set!! For now we always need the referee to manually add all questions
            question_set = s.decode_defaults_or_define_questions(
                referee_socket.recv(256))
            referee_socket.sendall(s.encode_ack(
                "Received defualts or define question decision."))

            # Referee chooses questions
            if question_set == NUM_QUESTIONS:
                logger.info("Waiting for referee's self-defined questions.")
                question_confirmed, new_question = s.decode_question_or_confirm(
                    referee_socket.recv(2048))
                while not question_confirmed:
                    referee_socket.sendall(s.encode_ack(
                        "Referee's question received"))
                    self.__state.add_question(new_question)
                    question_confirmed, new_question = s.decode_question_or_confirm(
                        referee_socket.recv(2048))

                referee_socket.sendall(s.encode_ack(
                    "Referee's confirmatino on questions received"))
                referee_socket.sendall(s.encode_questions(
                    self.__state.get_questions()))
            else:
                question_set = self.__state.choose_question_set(question_set)
                referee_socket.sendall(s.encode_questions(question_set))

            # Referee choose to start game
            s.decode_referee_startgame(referee_socket.recv(1024))
            self.__state.signal_game_start()

            while True:
                pass
        except Exception as e:
            print(e)
            information = self.__state.get_socket_addr(socket_addr)
            logger.error("Lost the connection with %s", information)
        finally:
            logger.info("Disconnecting %s (referee)", socket_addr)
            self.__state.remove_referee()

    #
    # Broadcast messages to players when enforcing strict synchronization in certain stages.
    # i.e., no other messages should arrive / be sent during the broadcast
    #
    def broadcast_with_ack(self, summary: str, encoded_message: bytes):
        player_sockets = self.__state.get_all_player_sockets_with_locks()
        for name, player_socket, lock in player_sockets:
            with lock:
                player_socket.sendall(encoded_message)
        for name, player_socket, lock in player_sockets:
            with lock:
                _ack = s.decode_ack(player_socket.recv(1024))  # Receiving ack
                logger.info(
                    "Sync - Broadcasted {%s} to Player {%s}", summary, name)
                # TODO: keep it safe in one lock -> otherwise the player_listnere might grab the lock and message won't be recognized
                # TODO: but we should try to mae it more concurrent
                # TODO: Try to move the broacasting questions and game start to each player thread? use barriers??

    #
    # Broadcast messages to players when there's no need to hear back from players.
    #
    def broadcast_without_ack(self, summary: str, encoded_message: bytes):
        player_sockets = self.__state.get_all_player_sockets_with_locks()
        for name, player_socket, lock in player_sockets:
            with lock:
                player_socket.sendall(encoded_message)
                logger.info(
                    "Async - Broadcasted {%s} to Player {%s}", summary, name)

    def send_full_leadersboard(self):
        logger.debug("Full leaderboard is %s", self.__state.get_leadersboard())
        with self.__state.referee_lock:
            self.__state.get_referee()[0].sendall(s.encode_leadersboard(
                self.__state.get_leadersboard()))
        logger.info("Sent leadersboard to Referee")

    def receive_player_name(self, player_socket: socket, player_lock: threading.Lock):
        logger.debug("Decoding name")
        player_name = s.decode_name(player_socket.recv(2048))
        with player_lock:
            player_socket.sendall(s.encode_name_response())

            return player_name


if __name__ == "__main__":
    hostname = socket.gethostname()
    IP = socket.gethostbyname_ex(hostname)[-1][-1]
    PORT = 5556
    Server(IP, PORT).start()
