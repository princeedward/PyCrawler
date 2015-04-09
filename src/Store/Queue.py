import collections

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

    def append(self, val):
        self.mem_queue_.append(val)

    def pop(self):
        return self.mem_queue_.popleft()

    def top(self):
        return self.mem_queue_[0]

    def __len__(self):
        return len(self.mem_queue_)
