import unittest
from cqueue import cQueue
from setting import PARAM
import multiprocessing


class testCQueue(unittest.TestCase):

    def test_normal_queue(self):
        param = PARAM
        test_queue = cQueue(param)
        start_flag = multiprocessing.Event()
        class test_process(multiprocessing.Process):
            def __init__(self, job_queue, others):
                self._job_queue = job_queue
                self._start = others[0]

            def run(self):
                self._start.wait()
