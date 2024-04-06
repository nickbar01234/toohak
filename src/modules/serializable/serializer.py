'''
Message format:
    {
        'action': 'connect | name | questions | update',
        'msg': string
    }
'''

CONNECT_SUCCESS_MSG = {'action': "connect", 'msg': "success"}

class ConnectionError(Exception):
    pass
class MessageNotRecognized(Exception):
    pass
class MessageNotForCurrentPhase(Exception):
    pass

import pickle
'''
Message Protocol for establishing connection
'''
def encode_connect_success():
    msg = CONNECT_SUCCESS_MSG
    return pickle.dumps(msg)

def encode_name(name: str):
    msg = {'action': "name", 'msg': name}
    return pickle.dumps(msg)

def decode_name(data: bytes) -> str:
    decoded = pickle.loads(data)
    match decoded:
        case {'action': "name", 'msg': name}:
            return name 
        case _:
            return ""

def decode_response(data: bytes, action: str) -> bool:
    decoded = pickle.loads(data)
    match decoded:
        case {'action': action2, 'msg': "success"}:
            return action2 == action
        case _:
            return False

def decode_connect_response(data: bytes) -> bool:
    return decode_response(data, "connection")

def decode_name_response(data: bytes) -> bool:
    return decode_response(data, "name")




'''
TODO: discuss - in general, when mismatch, should the serializer 
                            raise exception or log errors or return bool?

def decode_connect(data: bytes) -> bool:
    decoded_msg = pickle.loads(data)
    match decoded_msg:
        case {'action': "connect", 'msg': "success"}:
            return True
        case {'action': "connect", 'msg': _}:
            return False
        case {'action': _, 'msg': _}:
            raise MessageNotForCurrentPhase(str(decoded_msg))
        case _:
            raise MessageNotRecognized(str(decoded_msg))

'''