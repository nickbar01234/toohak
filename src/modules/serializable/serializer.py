import logging
logger = logging.getLogger(__name__)
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

'''
Message format:
    {
        'action': 'connect | name | questions | update',
        'msg': string
    }
'''
CONNECT = 'connect'
NAME = 'name'
SUCCESS = 'success'
QUESTIONS = 'questions'
UPDATE = 'update'

class InvalidMessageError(Exception):
    pass

import pickle
def encode(action, msg):
    msg = {"action": action, 'msg': msg}
    return pickle.dumps(msg)

def decode(data: bytes, action: str):
    decoded = pickle.loads(data)
    match decoded:
        case {'action': action2, 'msg': msg} if action2 == action:
            logger.debug("Decoding msg: " + str(msg))
            return msg 
        case msg:
            logger.error(f"Received message unrecognized / not for the current phase: {msg}")
            raise InvalidMessageError

'''
Message Protocol for establishing connection
'''
def encode_connect_success():
    return encode(CONNECT, SUCCESS)

def encode_name_response():
    return encode(NAME, SUCCESS)

def encode_name(name: str):
    return encode(NAME, name)

def decode_name(data: bytes) -> str:
    return decode(data, NAME)

def decode_response(data: bytes, action: str) -> bool:
    return decode(data, action) == SUCCESS

def decode_connect_response(data: bytes) -> bool:
    return decode_response(data, CONNECT)

def decode_name_response(data: bytes) -> bool:
    return decode_response(data, NAME)


'''
Message Protocol for distributing questions TODO: testing
'''
def encode_questions(questions):
    return encode(QUESTIONS, questions)

def decode_questions(data):
    return decode(data, QUESTIONS)

'''
Message Protocol for updating leaders' board TODO: testing
'''
def encode_leadersboard(top5players):
    return encode(UPDATE, top5players)

def decode_leadersboard(data):
    return decode(data, UPDATE) 


