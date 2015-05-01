import unittest
import multiprocessing
from asyncdns import DnsCacher, DnsBuffer
from test.sample_urls import domains


class testAdnsProcess(unittest.TestCase):

    def test_async_dns(self):
        # test the start of the independent thread
        dns_c = DnsCacher()

        # test concurrent submittions
        def worker(url):
            dns_bf = DnsBuffer()
            dns_bf.submit(url)
        pool = multiprocessing.Pool(100)
        pool.map_async(worker, domains)

        # test concurrent queries
        def worker2(url):
            dns_bf = DnsBuffer()
            dns_bf.require(url)
        pool.map_async(worker2, domains)
        # test process termination
        dns_c.close()
        # test different ports

    def test_async_dns_cornercases(self):
        # test the behavior of the DnsBuffer when DnsCacher halted
        # Format of the submitted domains
        pass
