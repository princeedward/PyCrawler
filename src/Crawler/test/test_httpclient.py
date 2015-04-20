import unittest
from httpclient import HttpClient, RelativeURIError, ServerNotFoundError
from setting import PARAM
from multiprocessing import Pool

class testHttpclient(unittest.TestCase):

    def test_basicConnections(self):
        httpclient = HttpClient()
        # test for available hosts
        avalaible_hosts = ["google.com", "facebook.com", "youtube.com",
                           "baidu.com", "yahoo.com", "wikipedia.org",
                           "amazon.com", "twitter.com", "taobao.com", "qq.com",
                           "google.co.in", "live.com",
                           "linkedin.com", "sina.com.cn", "weibo.com",
                           "yahoo.co.jp", "tmall.com", "google.co.jp",
                           "ebay.com", "t.co"]
        for each_url in avalaible_hosts:
            with self.assertRaises(RelativeURIError):
                resp, content = httpclient.request(each_url, method="HEAD")
        for each_url in avalaible_hosts:
            resp, content = httpclient.request("".join(["http://", each_url]),
                                       method="HEAD")
            # This cannot be enhanced by the library
            # self.assertEqual(len(content), 0)
        # test for none available hosts
        not_available = ["goggleb.com", "githude.com", "modlabcc.net"]
        for each_url in not_available:
            with self.assertRaises(RelativeURIError):
                resp, content = httpclient.request(each_url, method="HEAD")
        for each_url in not_available:
            with self.assertRaises(ServerNotFoundError):
                resp, content = httpclient.request("".join(["http://", each_url]),
                                           method="HEAD")
        # test headers
        param = PARAM
        headers = {"User-Agent": "cis455/penn/crawler/0.1",
                "Connection": "keep-alive",
                "Accept-Language": ";".join([",".join(list(param["language"])),
                                            "q=0.9"]),
                "Accept": ";".join([",".join(list(param["filetypes"])),
                                    "q=0.9"]),
                }
        resp, content = httpclient.request("https://www.uber.com/")
        # test redirection url
        resp, content = httpclient.request("http://www.github.com")
        self.assertTrue("content-location" in resp)
        self.assertTrue("http" in resp["content-location"])
        self.assertNotEqual("http://www.github.com", resp["content-location"])
        resp, content = httpclient.request("http://www.seas.upenn.edu/~yunkai/")
        self.assertTrue("content-location" in resp)
        self.assertTrue("http" in resp["content-location"])
        self.assertEqual("http://www.seas.upenn.edu/~yunkai/", resp["content-location"])

    def test_concurrentRequests(self):
        # test concurrent visit different websites
        avalaible_hosts = ["google.com", "facebook.com", "youtube.com",
                           "baidu.com", "yahoo.com", "wikipedia.org"]
        def worker(url):
            httpclient = HttpClient()
            httpclient.request("".join(["http://", url]), method="HEAD")
        a_pool = Pool(5)
        a_pool.map_async(worker, avalaible_hosts)
        # test concurrent visit same websites
        avalaible_hosts = ["www.seas.upenn.edu/~yunkai/" for i in xrange(10)]
        a_pool.map_async(worker, avalaible_hosts)

    def test_dnsResolving(self):
        # TODO: Implement this test when the module support this feature
        pass
