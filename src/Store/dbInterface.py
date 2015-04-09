from abs import ABCMeta, abstractmethod

class dbInterface(metaclass=ABCMeta):
    '''This is an abstract class which each nosql database module should
    implement at least the following methods:
        1. add: add a key-value pair to the database
        2. get: get value by specifying the key
    Extra requirements:
        1. Check database openablity, if not openable then throw ValueError
    '''
    def __init__(self, location, port):
        self.location = location
        self.port = port

    # @param key an object - must be serializable
    # @param value an object - must be serializable
    @abstractmethod
    def add(self, key, value):
        pass
    # @param key an object - must be serializable
    # @return The value object
    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def close(self):
        pass

    # @param key An object - must be serialization
    # @return boolean, True for key value pair exists in the database
    @abstractmethod
    def has(self, key):
        pass

