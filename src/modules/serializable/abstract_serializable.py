'''
Abstract class of a serializable instance
'''

from abc import ABC, abstractmethod


class AbstractSerializable(ABC):
    '''
    Abstract serializable instance
    '''
    @abstractmethod
    def serialize(self):
        '''
        Convert instance to string.
        '''
