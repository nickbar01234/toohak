import threading
import socket
from ..question.type import abstract_question

Name = str
Addr = str
Socket = socket.socket
SocketAddr = tuple[Socket, Addr]
Lock = threading.Lock
PlayerProgress = list[bool]
PlayerStates = dict[tuple[Socket, Addr],
                    tuple[Name, PlayerProgress, Lock, Lock]]
LeadersBoard = list[tuple[Name, int]]
Results = list[tuple[Name, int, int]]  # (name, correct, elapsed)
Question = abstract_question.AbstractQuestion
