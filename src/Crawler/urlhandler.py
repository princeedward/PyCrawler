# Modulerize this file for further customize
from .fetcher import Job
import re


def UrlHandler(url, param):
    # Apply url filtering
    if not SingleUrlFilter(url, param):
        return


# Url piece-wise filtering
# @param url a string of abosulate/relative url
# @param param A dictionary of parameters
def SingleUrlFilter(url, param):
    if ("#" in url) or ("http" not in url):
        return False
    if re.match("", url):
        return True
    else:
        return False
