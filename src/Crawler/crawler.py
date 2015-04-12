from multiprocessing import Pool, Queue, SyncManager
from .fetcher import Fetcher, Status
from .cqueue import cQueue


class CrawlManager(SyncManager):
    pass

CrawlManager.register('cQueue', cQueue)


class Crawler:

    def __init__(self, param):
        self.param = param
        self.terminate_flag = False
        if self.param["parallel"] == 2:
            self.process_pool = Pool(process=self.param["processnum"])
            self.manager = CrawlManager()
            self.manager.start()
            # Use to monitor the status of the child process and mange job
            # allocation
            self.process_monitor = self.manager.Queue()
            for i in xrange(self.param["processnum"]):
                self.process_monitor.put(Status(200))
            self.working_queue = self.manager.cQueue()

    def run(self):
        if self.param["parallel"] == 2:
            while not self.terminate_flag:
                # Noneblocking check
                if self.working_queue.empty():
                    continue
                if self.process_monitor.empty():
                    continue
                process_status = self.process_monitor.get()
                job = self.working_queue.get()
                self.process_pool.apply_async(
                    Fetcher,
                    args=(
                        job,
                        self.param,
                        self.working_queue,
                        self.process_monitor))
        elif self.param["parallel"] == 1:
            pass
        elif self.param["parallel"] == 0:
            pass
        else:
            raise ValueError("Parallel configuration is not recognized")

    def close(self):
        self.terminate_flag = True
