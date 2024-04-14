import logging
import socket
import threading
from modules import serializer as s
from modules import ServerState

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
        logger.info("Thread started to monitor the game_starting state.")

        self.__state.wait_game_start()
        logger.info("Game started")

        self.broadcast_with_ack("distribute questions", s.encode_questions(
            self.__state.get_questions()))

        # Broadcast to all players that the game has started TODO: how do we make sure all player threads have unblocked at this point?
        init_top5players = [(n, 0)
                            for n in self.__state.get_all_player_names()[:5]]
        self.broadcast_with_ack(
            "game starts", s.encode_startgame(init_top5players))

        for address in self.__state.get_all_socket_addr():
            self.__state.player_signal_start_game(address)

    def listener(self, client: socket.socket, addr):
        try:
            logger.info("Listening from %s", addr)
            client.sendall(s.encode_connect_success())
            role_selection = s.decode_role(client.recv(2048))
            client.sendall(s.encode_role_response())
            match role_selection:
                case "player":
                    return self.player_listener(client, addr)
                case "referee":
                    return self.referee_listener(client, addr)
        finally:
            client.close()

    # For each listener's thread to receive message form a specific player

    def player_listener(self, player_socket: socket.socket, player_addr):
        socket_addr = (player_socket, player_addr)
        player_lock = threading.Lock()
        try:
            logger.info(
                "Listener thread started to listen from %s", player_addr)

            # finalize establishing connection by receiving player's name
            # may raise InvalidMessage exception

            player_name = self.receive_player_name(player_socket, player_lock)
            # player_name = s.decode_name(player_socket.recv(2048))
            # with player_lock:
            #     player_socket.sendall(s.encode_name_response())

            self.__state.add_player(
                player_socket, player_addr, player_name, player_lock)

            # Wait for game starts TODO: does the listender thread need to block until game starts? maybe not?
            self.__state.player_wait_start_game(socket_addr)

            for _ in range(len(self.__state.get_questions())):
                logger.debug(
                    "Waiting to receive update from the player %s", player_name)
                progress = s.decode_progress(player_socket.recv(2048))
                logger.info("Receive %s from %s", progress, player_name)
                self.__state.update_player_progress(socket_addr, progress)
                if (top5 := self.__state.update_top5()):
                    self.broadcast_without_ack(
                        "new top5", s.encode_leadersboard(top5))

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
        except Exception as e:
            print(e)
            information = self.__state.get_socket_addr(socket_addr)
            logger.error("Lost the connection with %s", information)
        finally:
            logger.info("Disconnecting %s", socket_addr)
            self.__state.remove_player(socket_addr)

    def referee_listener(self, referee_socket: socket.socket, referee_addr):
        try:
            logger.info(
                "Referee thread started to listen from %s", referee_addr)

            s.decode_referee_startgame(referee_socket.recv(1024))
            self.__state.signal_game_start()

            while True:
                pass
        finally:
            return

    #
    # Broadcast messages to players when enforcing strict synchronization in certain stages.
    # i.e., no other messages should arrive / be sent during the broadcast
    #

    def broadcast_with_ack(self, summary, encoded_message):
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
    def broadcast_without_ack(self, summary, encoded_message):
        player_sockets = self.__state.get_all_player_sockets_with_locks()
        for name, player_socket, lock in player_sockets:
            with lock:
                player_socket.sendall(encoded_message)
                logger.info(
                    "Async - Broadcasted {%s} to Player {%s}", summary, name)

    def receive_player_name(self, player_socket: socket, player_lock: threading.Lock):
        player_name = s.decode_name(player_socket.recv(2048))
        with player_lock:
            player_socket.sendall(s.encode_name_response())

        return player_name


if __name__ == "__main__":
    hostname = socket.gethostname()
    IP = socket.gethostbyname_ex(hostname)[-1][-1]
    PORT = 5555
    Server(IP, PORT).start()
