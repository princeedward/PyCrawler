from abc import ABCMeta, abstractmethod


class dbInterface:

    '''This is an abstract class which each nosql database module should
    implement at least the following methods:
        1. add: add a key-value pair to the database
        2. get: get value by specifying the key
    Extra requirements:
        1. Check database openablity, if not openable then throw ValueError
    '''
    __metaclass__ = ABCMeta

    # @param param a diction of parameters
    @abstractmethod
    def __init__(self, param):
        pass

    # @param key an object - must be serializable
    # @param value an object - must be serializable
    @abstractmethod
    def add(self, key, value):
        pass

    # @param key an object - must be serializable
    # @param mapping a python dict object
    @abstractmethod
    def adddict(self, key, mapping):
        pass

    # @param key an object - must be serializable
    # @return The value object
    @abstractmethod
    def get(self, key):
        pass

    # @param key the key of the dictoinary
    # @param secondkey the key of the value inside dictionary
    @abstractmethod
    def getdict(self, key, secondkey):
        pass

    @abstractmethod
    def close(self):
        pass

    # @param key An object - must be serialization
    # @return boolean, True for key value pair exists in the database
    @abstractmethod
    def has(self, key):
        pass

    # @param key An object stored in the database
    # @return True if key exists and delete successfully
    @abstractmethod
    def delete(self, key):
        pass
