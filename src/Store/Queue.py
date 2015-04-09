import collections
import threading

class Queue:
    ''' This queue data structure suppose to implement on the top of in memmory
    database like redis, which can handle  the data do not fit in memory
    situation. This queue may be reimplemented to fulfill the deisgn purpose'''
    # TODO: This is currently a naive implementation which doesn't save the
    # queue to database if cannot fit into memory
    def __init__(self, init_list = []):
        if len(init_list) == 0:
            self.mem_queue_ = collections.deque()
        else:
            self.mem_queue_ = collections.deque(init_list)
        # In this perticular case, deque is thread safe, lock is unneccessary
        self.mutex_ = threading.Lock()
        self.unfinished_ = 0

    def append(self, val):
        with self.mutex_:
            self.mem_queue_.append(val)
            self.unfinished_ += 1

    def pop(self):
        with self.mutex_:
            self.unfinished_ -= 1
            result = self.mem_queue_.popleft()
        return result

    def top(self):
        with self.mutex_:
            result = self.mem_queue_[0]
        return result

    def __len__(self):
        return self.unfinished_

