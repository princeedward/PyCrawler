# This is a queue data structure wrapper
# The cQueue class in this module will be used to store the jobs
# And manage the politeness of the crawler
# This module later will provide a independent sockectserver which will run on a
# single process to provide memmory usage efficiency
from multiprocessing import Queue
from time import gmtime, mktime
from Store.NoSQL import NoSQL


class cQueue(Queue):

    def __init__(self, param):
        Queue.__init__(self)
        self._cached_domain = {}
        self._rules = NoSQL(param["database"]["engine"],
                            {"host": param["database"]["host"],
                             "port": param["database"]["port"],
                             "db": param["database"]["db"]["robot"]})

    def put(self, obj, block=True, timeout=None):
        Queue.put(self, obj, block, timeout)

    def get(self, block=True, timeout=None):
        # this is a naive queue implmentation
        # Check the domain crawling record
        # If the politeness constraints are not satisfied
        # Put the job at the end of the queue

        # This may cause uneccessary block
        while True:
            job = Queue.get(self, block, timeout)
            current_time = gmtime()
            domain = job.host
            if not domain or domain not in self._cached_domain:
                # query the robots.txt file first and return the job
                self._cached_domain[domain] = current_time
                return job
            last_visit = self._cached_domain[domain]
            time_diff = mktime(current_time) - mktime(last_visit)
            if time_diff >= self._rules.dictget(domain, "interval"):
                self._cached_domain[domain] = current_time
                return job
            else:
                Queue.put(self, job)
