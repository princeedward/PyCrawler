import unittest
from contentsave import SaveAndStatistics
from fetcher import Job
from httpclient import HttpClient
from setting import PARAM
import os
os.sys.path.append(PARAM["basedir"])
from Store.NoSQL import NoSQL


class testSaveAndStatistics(unittest.TestCase):

    def test_normal_functionality(self):
        url = "http://www.seas.upenn.edu/~yunkai/"
        new_job = Job(url, {})
        h = HttpClient()
        resp, content = h.request(url)
        param = PARAM
        SaveAndStatistics(new_job, content, param,
                          response_header=resp,
                          url_cache={"last-modified":
                                         "Wed, 22 Apr 2015 20:13:17 GMT"}
                         )
        db = NoSQL(param["database"]["engine"],
                   {"host": param["database"]["host"],
                    "port": param["database"]["port"],
                    "db": param["database"]["db"]["content"]})
        self.assertEqual(db.dictget(new_job.identifier, "content"), content)
        self.assertEqual(db.dictget(new_job.identifier, "url"), new_job.url)
