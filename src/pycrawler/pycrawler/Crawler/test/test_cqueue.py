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

    def run(self):
        self._start.wait()
        count = 0
        while count < 5:
            job = self._job_queue.get()
            count += 1
            self._job_queue.put(job, block=True)
        self._job_queue.close()


class testCQueue(unittest.TestCase):

    def test_multiprocessing_queue(self):
        param = PARAM
        # initializing the queue
        test_queue = cQueue(param)
        for each in domains[:20]:
            new_job = Job("".join(["http://", each]), {})
            test_queue.put(new_job)
        start_flag = multiprocessing.Event()

        # test the queue in the multiprocessing settings
        a_list_of_processes = [test_process(test_queue, [start_flag])
                               for i in xrange(4)]
        for each in a_list_of_processes:
            each.start()

        start_flag.set()

        for each in a_list_of_processes:
            each.join()


if __name__ == "__main__":
    unittest.main()
