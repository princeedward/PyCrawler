import unittest
import httplib2
import Queue
from pycrawler.Crawler.fetcher import Job, HtmlUrlExtractor, TextUrlExtractor, \
    UrlExtractor, Fetcher
from pycrawler.Crawler.setting import PARAM
from pycrawler.Crawler.asyncdns import DnsCacher


class testFetcher(unittest.TestCase):

    def test_Job(self):
        new_job = Job("http://github.com", {})
        self.assertTrue(isinstance(new_job.url, str))
        self.assertTrue(isinstance(new_job.identifier, str))
        self.assertTrue(isinstance(new_job.host, str))

    def test_HtmlUrlExtractor(self):
        h = httplib2.Http()
        extract_url = 'http://www.seas.upenn.edu/~yunkai/'
        resp_header, resp_body = h.request(extract_url)
        urls = HtmlUrlExtractor(resp_body)
        for each_url in urls:
            self.assertTrue(isinstance(each_url, str))
        urls = HtmlUrlExtractor(resp_body, root_url=extract_url)
        for each_url in urls:
            self.assertTrue(isinstance(each_url, str))
            self.assertTrue("http" in each_url)

    def test_TextUrlExtractor(self):
        pass

    def test_UrlExtractor(self):
        pass

    def test_Fetcher_single_process(self):
        new_job = Job('http://www.seas.upenn.edu/~yunkai/', {})
        param = PARAM
        work_queue = Queue.Queue()
        work_monitor = Queue.Queue()
        adns_cacher = DnsCacher()
        try:
            Fetcher(new_job, param, work_queue, work_monitor)
            job_status = work_monitor.get()
            self.assertEqual(job_status.status, 200)
            while not work_queue.empty():
                each = work_queue.get()
                self.assertTrue(isinstance(each, Job))
                self.assertTrue('http' in each.url)
        finally:
            adns_cacher.close()


def main():
    unittest.main()

if __name__ == "__main__":
     main()
