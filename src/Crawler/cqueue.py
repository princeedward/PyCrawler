# This is a queue data structure wrapper
from multiprocessing import Queue


class cQueue(Queue):

    def __init__(self):
        Queue.__init__(self)

    def put(self, obj, block=True, timeout=None):
        Queue.put(self, obj, block, timeout)

    def get(self, block=True, timeout=None):
        Queue.get(self, block, timeout)
