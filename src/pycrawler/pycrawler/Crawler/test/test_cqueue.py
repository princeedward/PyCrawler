import unittest
import multiprocessing
from pycrawler.Crawler.cqueue import cQueue
from pycrawler.Crawler.setting import PARAM
from pycrawler.Crawler.fetcher import Job
from sample_urls import domains


# define the process class
class test_process(multiprocessing.Process):

    def __init__(self, job_queue, others):
        multiprocessing.Process.__init__(self)
        self._job_queue = job_queue
        self._start = others[0]
        self._finished = others[1]

    def run(self):
        self._start.wait()
        count = 0
        while count < 5:
            job = self._job_queue.get()
            count += 1
            self._job_queue.put(job, block=True)
        self._job_queue.close()
        self._finished.set()
        print "process finished"


class testCQueue:  # (unittest.TestCase):

    def test_multiprocessing_queue(self):
        param = PARAM
        # initializing the queue
        test_queue = cQueue(param)
        for each in domains:
            new_job = Job("".join(["http://", each]), {})
            test_queue.put(new_job)
        start_flag = multiprocessing.Event()
        finished_flag = multiprocessing.Event()

        # test the queue in the multiprocessing settings
        a_list_of_processes = [test_process(test_queue, [start_flag, finished_flag])
                               for i in xrange(1)]
        for each in a_list_of_processes:
            each.start()

        start_flag.set()

        finished_flag.wait()
        test_queue.close()

        for each in a_list_of_processes:
            print "Waiting for terminating"
            each.join()
        print "Fnihsed join()"


if __name__ == "__main__":
    # unittest.main()
    a = testCQueue()
    a.test_multiprocessing_queue()
