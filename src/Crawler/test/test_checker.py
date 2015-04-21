import os
from setting import PARAM
os.sys.path.append(PARAM["basedir"])
import unittest
from checker import UrlChecker
from fetcher import Job
from httpclient import HttpClient
from Store.NoSQL import NoSQL


class testUrlChecker(unittest.TestCase):

    def test_mainfunctionality(self):
        param = PARAM
        test_db = NoSQL(param["database"]["engine"],
                        {"host": param["database"]["host"],
                         "port": param["database"]["port"],
                         "db": param["database"]["db"]["urlcache"]})
        url = "http://www.seas.upenn.edu/~yunkai/"
        # clear cache and other initilization
        del_job = Job(url, {})
        test_db.delete(del_job.identifier)  # TODO: This needs to be supported
        # test none cached url
        job_parameters = {}
        test_job = Job(url, job_parameters)
        h = HttpClient()
        header, _ = h.request(url, method="HEAD")
        header["last-modified"] = "Tue, 19 Apr 2015 02:33:38 GMT"
        cached, result = UrlChecker(test_job, param, header)
        self.assertFalse(cached)
        self.assertEqual(result["url"], url)
        # test cached url
        cached, result = UrlChecker(test_job, param, header)
        self.assertTrue(cached)
        self.assertEqual(result["url"], url)
        header["last-modified"] = "Tue, 21 Apr 2015 02:33:38 GMT"
        cached, result = UrlChecker(test_job, param, header)
        self.assertFalse(cached)
        # test the different url with same identifier (This is rare)
        test_job.url = """https://alliance.seas.upenn.edu/~cis520/wiki/\
            index.php?n=Lectures.Lectures"""
        cached, result = UrlChecker(test_job, param, header)
        self.assertFalse(cached)
        self.assertEqual(result["url"], test_job.url)
