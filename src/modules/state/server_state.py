import logging
import socket
import threading
from ..type.aliases import *
from ..serializable import serializer as s
from ..question.multiple_choice_question_builder import MultipleChoiceQuestionBuilder
from ..solution.multiple_choice_solution_builder import MultipleChoiceSolutionBuilder

logger = logging.getLogger()
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

# Mock the set of questions TODO: remove once we have an actual set of questions
#
# default question sets
#
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

cs_questions = [
    MultipleChoiceQuestionBuilder()
    .add_question("What is the purpose of virtual memory in operating systems?")
    .add_option("To allow multiple programs to run simultaneously")
    .add_option("To provide a larger address space than physical memory")
    .add_option("To improve the performance of disk I/O operations")
    .add_option("To protect the operating system from malicious software")
    .add_solution(MultipleChoiceSolutionBuilder().add_solution("To provide a larger address space than physical memory").build())
    .build(),


    MultipleChoiceQuestionBuilder()
    .add_question("Which of the following is a key characteristic of the TCP protocol?")
    .add_option("Connectionless communication")
    .add_option("Guaranteed delivery of packets")
    .add_option("Minimal overhead")
    .add_option("Limited scalability")
    .add_solution(MultipleChoiceSolutionBuilder().add_solution("Guaranteed delivery of packets").build())
    .build(),

    MultipleChoiceQuestionBuilder()
    .add_question("What is the purpose of the "fork()" system call in Unix-like operating systems?")
    .add_option("To create a new process")
    .add_option("To allocate memory for a new process")
    .add_option("To terminate a process")
    .add_option("To wait for a child process to terminate")
    .add_solution(MultipleChoiceSolutionBuilder().add_solution("To create a new process").build())
    .build(),

    MultipleChoiceQuestionBuilder()
    .add_question("Which sorting algorithm has the best worst-case time complexity?")
    .add_option("Bubble sort")
    .add_option("Quick sort")
    .add_option("Merge sort")
    .add_option("Insertion sort")
    .add_solution(MultipleChoiceSolutionBuilder().add_solution("Merge sort").build())
    .build(),

]

iq_questions = [
    MultipleChoiceQuestionBuilder()
    .add_question("What comes next in the sequence? 2, 6, 12, 20, ?")
    .add_option("30")
    .add_option("24")
    .add_option("36")
    .add_option("42")
    .add_solution(MultipleChoiceSolutionBuilder().add_solution("30").build())
    .build(),

    MultipleChoiceQuestionBuilder()
    .add_question("If all Feps are Leps, and some Leps are Peps, then some Feps are definitely Peps.")
    .add_option("True")
    .add_option("False")
    .add_solution(MultipleChoiceSolutionBuilder().add_solution("False").build())
    .build(),

    MultipleChoiceQuestionBuilder()
    .add_question("If 6+4=210, 9+2=711, and 8+5=313, then 5+2=?")
    .add_option("612")
    .add_option("513")
    .add_option("307")
    .add_option("811")
    .add_solution(MultipleChoiceSolutionBuilder().add_solution("307").build())
    .build(),

    MultipleChoiceQuestionBuilder()
    .add_question("Which of these is the largest species of penguin?")
    .add_option("Emperor")
    .add_option("King")
    .add_option("Adelie")
    .add_option("Chinstrap")
    .add_solution(MultipleChoiceSolutionBuilder().add_solution("Emperor").build())
    .build(),

    MultipleChoiceQuestionBuilder()
    .add_question("Which country is the largest producer of coffee in the world?")
    .add_option("Colombia")
    .add_option("Ethiopia")
    .add_option("France")
    .add_option("Brazil")
    .add_solution(MultipleChoiceSolutionBuilder().add_solution("Brazil").build())
    .build(),

    MultipleChoiceQuestionBuilder()
    .add_question("Which city is not a capital city of a country?")
    .add_option("Zurich")
    .add_option("Prague")
    .add_option("Stockholm")
    .add_option("Budapest")
    .add_solution(MultipleChoiceSolutionBuilder().add_solution("Brazil").build())
    .build(),

]


class ServerState:
    def __init__(self, ip, port):
        self.__addr = (ip, port)

        self.__referee_sockets_lock = threading.Lock()
        self.__referee_sockets = []

        # players states
        self.__player_states_lock = threading.Lock()  # guard both states and top5
        self.__player_states: PlayerStates = {}
        self.__top5players: LeadersBoard = []

        # only main thread should access
        self.__listeners: list[threading.Thread] = []

        # game state / info
        self.__game_starts = threading.Semaphore(0)
        # for now: will be initialized after the playerCount is finalized
        self.__game_ends = None

        self.__questions = questions  # TODO: change later to receive from the referee
        self.__questions_lock = threading.Lock()

    def get_server_addr(self):
        return self.__addr

    def add_listener(self, listener):
        self.__listeners.append(listener)

    def add_player(self, psocket: Socket, paddr: Addr, pname: Name, plock: threading.Lock):
        logger.debug("Adding player {%s, %s, %s}", pname, psocket, paddr)

        with self.__player_states_lock:
            self.__player_states[(psocket, paddr)] = (
                pname, [], plock, threading.Semaphore(0))

        logger.info("Added player {%s, %s, %s}",
                    pname, psocket.getsockname(), paddr)

    def remove_player(self, socket_addr: SocketAddr):
        with self.__player_states_lock:
            if socket_addr in self.__player_states:
                del self.__player_states[socket_addr]
        logger.info("Removed connection from %s", socket_addr)

    def player_wait_start_game(self, socket_addr: SocketAddr):
        player = None
        with self.__player_states_lock:
            player = self.__player_states.get(socket_addr, None)
        if player is not None:
            player[-1].acquire()

    def player_signal_start_game(self, socket_addr: SocketAddr):
        with self.__player_states_lock:
            if socket_addr in self.__player_states:
                self.__player_states[socket_addr][-1].release()

    def num_players(self):
        with self.__player_states_lock:
            return len(self.__player_states)

    def update_player_progress(self, socket_addr: SocketAddr, new_progress: PlayerProgress):
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

    def get_socket_addr(self, addr: Addr):
        with self.__player_states_lock:
            return self.__player_states.get(addr, None)

    def get_questions(self):
        with self.__questions_lock:
            return self.__questions

    def set_questions(self, new_questions):
        with self.__questions_lock:
            self.__questions = new_questions

    def wait_game_start(self):
        self.__game_starts.acquire()

    def signal_game_start(self):
        self.__game_starts.release()
