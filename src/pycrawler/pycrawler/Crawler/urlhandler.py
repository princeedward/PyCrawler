# Modulerize this file for further customize
# from fetcher import Job
# import re
from urlparse import urlparse, urldefrag


def UrlHandler(url, param, options):
    # Apply url filtering
    filtered_url, domain = SingleUrlFilter(url, param)
    return filtered_url, {"domain": domain}


# Url piece-wise filtering
# @param url a string of abosulate/relative url
# @param param A dictionary of parameters
def SingleUrlFilter(url, param):
    result = urlparse(url)
    domain = result.netloc
    defraged_url = urldefrag(url)
    return defraged_url[0], domain
