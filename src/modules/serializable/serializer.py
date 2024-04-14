import pickle
from ..type.aliases import *

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

'''
Message format:
    {
        'action': 'connect | name | questions | start | leadersboard | individual_progress | end | leave',
        'msg': string
    }
'''
CONNECT = 'connect'
NAME = 'name'
SUCCESS = 'success'
START = 'start'
QUESTIONS = 'questions'
ACK = 'ack'
LEADERSBOARD = 'leadersboard'
INDIVIDUAL_PROGRESS = 'individual_progress'
END = 'end'
LEAVE = 'leave'


class InvalidMessageError(Exception):
    pass


def encode(action, msg):
    msg = {"action": action, 'msg': msg}
    return pickle.dumps(msg)


def decode(data: bytes, action: str):
    # logger.debug("Decoding binary: %s for %s", data, action)
    decoded = pickle.loads(data)
    match decoded:
        case {'action': action2, 'msg': msg} if action2 == action:
            return msg
        case msg:
            logger.error(
                "Received message unrecognized / not for the current phase: %s", msg)
            raise InvalidMessageError


#
# Message Protocol for establishing connection
#

def encode_connect_success():
    return encode(CONNECT, SUCCESS)


def encode_name_response():
    return encode(NAME, SUCCESS)


def encode_name(name: str):
    return encode(NAME, name)


def decode_name(data: bytes) -> Name:
    return decode(data, NAME)


def decode_response(data: bytes, action: str) -> bool:
    return decode(data, action) == SUCCESS


def decode_connect_response(data: bytes) -> bool:
    return decode_response(data, CONNECT)


def decode_name_response(data: bytes) -> bool:
    return decode_response(data, NAME)


#
# Message Protocol for distributing questions
#


def encode_questions(questions: list[Question]):
    return encode(QUESTIONS, questions)


def decode_questions(data: bytes) -> list[Question]:
    return decode(data, QUESTIONS)


def encode_ack(for_action: str):
    return encode(ACK, for_action)


def decode_ack(data: bytes):
    return decode(data, ACK)

#
# Message Protocol for server to signal players game start
#


# TODO: global type aliases
def encode_startgame(init_top5players: LeadersBoard):
    return encode(START, init_top5players)


def decode_startgame(data: bytes):
    return decode(data, START)

#
# Message Protocol for updating leaders' board TODO: testing
#

# TODO: global file to share type?


def encode_leadersboard(top5players: LeadersBoard):
    return encode(LEADERSBOARD, top5players)


def decode_leadersboard(data: bytes) -> LeadersBoard:
    return decode(data, LEADERSBOARD)


#
# Message Protocol for updating player's progress
#

def encode_progress(progress: PlayerProgress):  # TODO: global file to share type?
    return encode(INDIVIDUAL_PROGRESS, progress)


def decode_progress(data: bytes):
    return decode(data, INDIVIDUAL_PROGRESS)


#
# Message Protocol for the server to notify players that game ends
#

def encode_endgame():
    return encode(END, "")


def decode_endgame(data: bytes):
    return decode(data, END)

# returns (False, "") if game ends or (True, Leadersboard) if it's an update


def decode_update_or_endgame(data: bytes) -> tuple[bool, LeadersBoard]:
    decoded = pickle.loads(data)
    match decoded:
        case {'action': action, 'msg': msg} if action == END:
            logger.debug("Decoded message: game ends")
            return (False, [])
        case {'action': action, 'msg': msg} if action == LEADERSBOARD:
            logger.debug(f"Decoded message: leader's board - {str(msg)}")
            return (True, msg)
        case msg:
            logger.error(
                f"Received message unrecognized / not for the current phase: {msg}")
            raise InvalidMessageError


#
# Message Protocol for players to notify the server they're leaving
#


def encode_leave():
    return encode(LEAVE, "")


def decode_leave(data: bytes):
    return decode(data, LEAVE)
