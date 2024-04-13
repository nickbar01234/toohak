import logging
import socket
import threading
from ..serializable import serializer as s
from ..question.multiple_choice_question_builder import MultipleChoiceQuestionBuilder
from ..solution.multiple_choice_solution_builder import MultipleChoiceSolutionBuilder

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

Name = str
Addr = str
Socket = socket.socket
Lock = threading.Lock
PlayerProgress = list[bool]
PlayerStates = dict[tuple[Socket, Addr],
                    tuple[Name, PlayerProgress, Lock, Lock]]


class ServerState:
    def __init__(self, ip, port):
        self.__addr = (ip, port)

        self.__referee_sockets_lock = threading.Lock()
        self.__referee_sockets = []

        # players states
        self.__player_states_lock = threading.Lock()  # guard both states and top5
        self.__player_states: PlayerStates = {}
        self.__top5players: list[tuple[Name, int]] = []

        # only main thread should access
        self.__playerListeners: list[threading.Thread] = []

        # game state / info
        self.gameStarts = threading.Semaphore(0)
        self.__gameEnds = None  # for now: will be initialized after the playerCount is finalized

        self.__questions = questions  # TODO: change later to receive from the referee
        self.__questions_lock = threading.Lock()

    def get_server_addr(self):
        return self.__addr

    def add_listener(self, listener):
        self.__playerListeners.append(listener)

    def add_player(self, psocket, paddr, pname, plock):
        logger.debug("Adding player {%s, %s, %s}", pname, psocket, paddr)

        with self.__player_states_lock:
            self.__player_states[(psocket, paddr)] = (
                pname, [], plock, threading.Semaphore(0))

            # Hardcoding for now: start the game when 2 players joined
            # TODO: move this to where it's appropriate (referee should start the game instead)
            n_players = len(self.__player_states)
            if n_players == 2:
                # plus the server main thread
                self.gameStarts.release()

        logger.info("Added player {%s, %s, %s}",
                    pname, psocket.getsockname(), paddr)

    def remove_player(self, socket_addr):
        with self.__player_states_lock:
            if socket_addr in self.__player_states:
                del self.__player_states[socket_addr]
        logger.info("Removed connection from %s", socket_addr)

    def player_wait_start_game(self, socket_addr):
        player = None
        with self.__player_states_lock:
            player = self.__player_states.get(socket_addr, None)
        if player is not None:
            player[-1].acquire()

    def player_signal_start_game(self, socket_addr):
        with self.__player_states_lock:
            if socket_addr in self.__player_states:
                self.__player_states[socket_addr][-1].release()

    def num_players(self):
        with self.__player_states_lock:
            return len(self.__player_states)

    def update_player_progress(self, socket_addr, new_progress):
        with self.__player_states_lock:
            name, _, lock, game_start_lock = self.__player_states[socket_addr]
            self.__player_states[socket_addr] = name, new_progress, lock, game_start_lock
            logger.info(
                "Player {%s} progress has been updated: %s", name, new_progress)

    # Return the updated top5players if there's a non-trivial update, otherwise return None
    def update_top5(self):
        with self.__player_states_lock:
            name_progress_list = [(n, len(p))
                                  for n, p, l, _ in list(self.__player_states.values())]
            new_top5 = sorted(name_progress_list,
                              key=lambda x: x[1], reverse=True)[:5]
            logger.debug("The new top5 players are %s", new_top5)

            if new_top5 != self.__top5players:
                self.__top5players = new_top5
                return new_top5
            return None

    def get_all_player_names(self) -> list[Name]:
        with self.__player_states_lock:
            players = [n for (n, _, _, _) in list(
                self.__player_states.values())]
            logger.debug("Get all players: %s", players)
            return players

    def get_all_player_sockets_with_locks(self) -> list[tuple[Name, Socket, Lock]]:
        with self.__player_states_lock:
            player_sockets = [(n, s, l) for (s, _), (n, _, l, _)
                              in list(self.__player_states.items())]
            logger.debug("Get all %d player sockets", len(player_sockets))
            return player_sockets

    def get_all_socket_addr(self):
        with self.__player_states_lock:
            return list(self.__player_states.keys())

    def get_socket_addr(self, addr):
        with self.__player_states_lock:
            return self.__player_states.get(addr, None)

    def get_questions(self):
        with self.__questions_lock:
            return self.__questions

    def set_questions(self, new_questions):
        with self.__questions_lock:
            self.__questions = new_questions
