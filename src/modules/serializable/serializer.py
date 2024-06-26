import pickle
from ..type.aliases import *
import logging
from typing import Literal
from ..question.abstract_question_builder import AbstractQuestionBuilder

logger = logging.getLogger(__name__)
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)


type game_role = Literal["player"] | Literal["referee"]

'''
Message format:
    {
        'action': 'connect | name | questions | start | leadersboard | individual_progress | end | leave',
        'msg': string
    }
'''
CONNECT = 'connect'
ROLE = 'role'
NAME = 'name'
SUCCESS = 'success'
FAILURE = 'failure'
START = 'start'
SET = 'set'
QUESTION = 'question'
QUESTIONS = 'questions'
CONFIRM = 'confirm'  # referee confirm on the question set
ACK = 'ack'
LEADERSBOARD = 'leadersboard'
INDIVIDUAL_PROGRESS = 'individual_progress'
END = 'end'
LEAVE = 'leave'
ELAPSE_TIME = 'time'
QUIT = 'quit'

REFEREE_START_GAME = "referee_start"


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
                "Received message unrecognized / not for the current phase: %s, expecting %s", msg, action)
            raise InvalidMessageError


def decode_response(data: bytes, action: str) -> bool:
    return decode(data, action) == SUCCESS

#
# Message Protocol for establishing connection
#


def encode_connect_success():
    return encode(CONNECT, SUCCESS)


def decode_connect_response(data: bytes) -> bool:
    return decode_response(data, CONNECT)

#
# Message Protocol for sending name
#


def encode_name(name: str):
    return encode(NAME, name)


def decode_name(data: bytes) -> Name:
    return decode(data, NAME)


def encode_name_response(success: bool):
    return encode(NAME, SUCCESS if success else FAILURE)


def decode_name_response(data: bytes) -> bool:
    return decode_response(data, NAME)

#
# Message Protocol for sending client role (player/referee)
#


def encode_role(role: game_role):
    logger.info("Game role %s", role)
    return encode(ROLE, role)


def decode_role(data: bytes) -> game_role:
    return decode(data, ROLE)


def encode_role_response(status):
    return encode(ROLE, status)


def decode_role_response(data: bytes) -> bool:
    return decode_response(data, ROLE)

#
# Message Protocol for distributing questions
#


def encode_defaults_or_define_questions(idx: int):
    return encode(SET, idx)


def decode_defaults_or_define_questions(data: bytes) -> int:
    return decode(data, SET)


def encode_question(question: Question):
    return encode(QUESTION, question)


def decode_question(data: bytes) -> Question:
    return decode(data, QUESTION)


def encode_questions(questions: list[Question]):
    return encode(QUESTIONS, questions)


def decode_questions(data: bytes) -> list[Question]:
    return decode(data, QUESTIONS)


def encode_ack(for_action: str):
    return encode(ACK, for_action)


def decode_ack(data: bytes):
    return decode(data, ACK)


def encode_confirm_questions():
    return encode(CONFIRM, "questions")
#
# Message Protocol for server to signal players game start
#


def encode_startgame(init_top5players: LeadersBoard):
    return encode(START, init_top5players)


def decode_startgame(data: bytes):
    return decode(data, START)

#
# Message Protocol for updating leaders' board
#


def encode_leadersboard(top5players: LeadersBoard):
    return encode(LEADERSBOARD, top5players)


def decode_leadersboard(data: bytes) -> LeadersBoard:
    return decode(data, LEADERSBOARD)


#
# Message Protocol for updating player's progress
#

def encode_progress(progress: PlayerProgress):
    return encode(INDIVIDUAL_PROGRESS, progress)


def decode_progress(data: bytes):
    return decode(data, INDIVIDUAL_PROGRESS)


#
# Message Protocol for the server to notify players that game ends
#

def encode_endgame(data: bytes):
    return encode(END, data)


def decode_endgame(data: bytes):
    return decode(data, END)

# returns (False, "") if game ends or (True, Leadersboard) if it's an update


def decode_update_or_endgame(data: bytes) -> tuple[bool, LeadersBoard]:
    decoded = pickle.loads(data)
    match decoded:
        case {'action': action, 'msg': msg} if action == END:
            logger.debug("Decoded message: game ends")
            return (False, msg)
        case {'action': action, 'msg': msg} if action == LEADERSBOARD:
            logger.debug(f"Decoded message: leader's board - {str(msg)}")
            return (True, msg)
        case msg:
            logger.error(
                f"Received message unrecognized / not for the current phase: {msg}")
            raise InvalidMessageError

# the boolean in the tuple indicates whether referee confirms on the current question set or not


def decode_question_or_confirm(data: bytes) -> tuple[bool, Question]:
    decoded = pickle.loads(data)
    match decoded:
        case {'action': action, 'msg': msg} if action == QUESTION:
            logger.debug("Decoded question: %s", msg)
            return (False, msg)
        case {'action': action, 'msg': msg} if action == CONFIRM:
            logger.debug("Decoded confirmation on the question set")
            return (True, None)
        case msg:
            logger.error(
                "Received message unrecognized / not for the current phase: %s", msg)
            raise InvalidMessageError

#
# Message Protocol for players to notify the server they're leaving
#


def encode_leave():
    return encode(LEAVE, "")


def decode_leave(data: bytes):
    return decode(data, LEAVE)


def encode_referee_startgame():
    return encode(REFEREE_START_GAME, "")


def decode_referee_startgame(data: bytes):
    return decode(data, REFEREE_START_GAME)


def encode_elapse_time(seconds: int):
    return encode(ELAPSE_TIME, seconds)


def decode_elapse_time(data: bytes) -> int:
    return decode(data, ELAPSE_TIME)


def encode_quit():
    return encode(QUIT, "")


def decode_quit(data: bytes):
    return decode(data, QUIT)
