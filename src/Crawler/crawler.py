from multiprocessing import Pool, Queue, Manager
from fetcher import fetcher


class Crawler:

    def __init__(self, param):
        self.param = param
        self.manager = Manager()

    def run(self):
        if self.param["parallel"] == 2:
            self.process_pool = Pool(process=self.param["processnum"])
            self.process_monitor = self.manager.Queue()
            while True:
                job = self.working_queue.get()
                self.process_pool.apply_async(
                    fetcher,
                    args=(
                        job,
                        self.param,
                        self.process_monitor))
        elif self.param["parallel"] == 1:
            pass
        elif self.param["parallel"] == 0:
            pass
        else:
            raise ValueError("Parallel configuration is not recognized")
