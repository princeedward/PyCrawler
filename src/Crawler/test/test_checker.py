import unittest
from checker import UrlChecker
from fetcher import Job
from setting import PARAM
from httpclient import HttpClient

class test_UrlChecker(unittest.TestCase):

    def test_mainfunctionality(self):
        param = PARAM
        # clear cache and other initilization
        # test none cached url
        # test cached url
        # test the different url with same identifier (This is rare)
