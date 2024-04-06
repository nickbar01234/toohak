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

class ConnectionError(Exception):
    pass
class MessageNotRecognized(Exception):
    pass
class MessageNotForCurrentPhase(Exception):
    pass

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

import pickle
def encode(action, msg):
    msg = {"action": action, 'msg': msg}
    return pickle.dumps(msg)

def decode(data: bytes):
    return pickle.loads(data)

def decode(data: bytes, action: str) -> str:
    decoded = pickle.loads(data)
    match decoded:
        case {'action': action2, 'msg': msg} if action2 == action:
            return msg 
        case msg:
            logger.error(f"Received message unrecognized / not for the current phase: {msg}")
            return ""

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
Message Protocol for distributing questions
'''


'''
Message Protocol for updating leaders' board
'''

'''
TODO: discuss - in general, when mismatch, should the serializer 
                            raise exception or log errors or return bool?

def decode_connect(data: bytes) -> bool:
    decoded_msg = pickle.loads(data)
    match decoded_msg:
        case {'action': "connect", 'msg': SUCCESS}:
            return True
        case {'action': "connect", 'msg': _}:
            return False
        case {'action': _, 'msg': _}:
            raise MessageNotForCurrentPhase(str(decoded_msg))
        case _:
            raise MessageNotRecognized(str(decoded_msg))

'''