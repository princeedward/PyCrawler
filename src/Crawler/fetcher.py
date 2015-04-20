import lxml.html as xhtml
import re
import hashlib
from urlparse import urlparse
from .checker import UrlChecker
from .httpclient import HttpClient, RelativeURIError, ServerNotFoundError
from .urlhandler import UrlHandler
from .asyncdns import DnsBuffer
from .urlregex import URL_REGEX
from contentsave import SaveAndStatistics


# This class indicate the status of the fetcher
class Status:

    # @param code Indicate the child process status
    #               200 Ready for job

    def __init__(self, code, message=None):
        self.status = code
        self.message = message


# This class is the job class which including the url to crawl and other
# information to boost the crawling
class Job:

    def __init__(self, url, params):
        self.url = url
        self.identifier = self.calculateID(self.url)
        if "host" in params:
            self.host = params["host"]
        else:
            parsed_url = urlparse(self.url)
            self.host = parsed_url.netloc
        self.host_ip = None

    def setLastUpdate(self, date):
        self.last_update = date

    def setUrl(self, url):
        self.url = url
        self.identifier = self.calculateID(self.url)

    def setIP(self, ip):
        self.host_ip = ip

    def calculateID(self, url):
        # TODO: Modularize this function
        h_func = hashlib.sha1()
        h_func.update(url)
        return h_func.hexdigest


def CheckContentType(type_str, allowed_types):
    for each_type in allowed_types:
        if each_type in type_str:
            return True
    return False

# TODO: In a future version, put this in the parameter
USER_AGENT = "penn/cis455/crawler/0.1"

# Fetcher function which runs in each child process


def Fetcher(job, param, works, monitor):
    # document size and document type check using response header
    # better with persistence connection
    http_client = HttpClient()
    headers = {"User-Agent": USER_AGENT,
               "Connection": "keep-alive",
               "Accept-Language": ";".join([",".join(list(param["language"])),
                                           "q=0.9"]),
               "Accept": ";".join([",".join(list(param["filetypes"])),
                                   "q=0.9"]),
               }
    try:
        resp_header, content = http_client.request(
            job.url, method="HEAD", headers=headers)
    except RelativeURIError:
        monitor.put(Status(401, "Url is not absolute"))
        return
    except ServerNotFoundError:
        monitor.put(Status(404, "Server is not found"))
        return
    except Exception as e:
        monitor.put(Status(500, e.message()))
        return
    # ----------- content filter -------------
    # check content type
    if "content-type" not in resp_header or not CheckContentType(
            resp_header["content-type"],
            param["filetypes"]):
        monitor.put(Status(402, "File type is not recognized"))
        return
    # check content size
    if "content-length" in resp_header and \
            int(resp_header["content-length"]) > param["maxsize"]:
        monitor.put(Status(403, "File size is too big"))
        return
    # ----------------------------------------
    # check the existence of the url last update (politeness handled by queue)
    job.setUrl(resp_header["content-location"])  # used the real url
    exist, records = UrlChecker(job, param, resp_header)
    if exist:
        monitor.put(Status(200, "Url exists and skiped"))
        return
    # Extract urls and create new jobs, submit dns resolve requests(async)
    # TODO: Think about this, whether this is necessary
    headers["Connection"] = "close"
    resp_header, content = http_client.request(
        job.url, method="GET", headers=headers)
    page_urls = UrlExtractor(content, param, works,
                             doc_type=resp_header["content-type"],
                             handle=UrlHandler, root_url=job.url)
    # do statistics and save the document and statistics (asyn)
    SaveAndStatistics(job, content, param,
                      response_header = resp_header,
                      url_cache = records
                      )
    # If job has been finished succesful, indicate the main process
    monitor.put(Status(200))


# A url extractor can extract urls in html/xml/text
# @param str_doc Document in string format
# @param doc_type Document type string
# @param handle Handle funtion wich will be called for each url extracted
# @param root_url Root url for extracting relative urls
# @return True for succeeded, False for fail
def UrlExtractor(str_doc, param, wqueue, doc_type="html",
                 handle=None, root_url=None):
    url_set = set()
    # Enable ip and port number input
    adns_checker = DnsBuffer()
    if "html" in doc_type:
        html_tree = xhtml.fromstring(str_doc)
        if root_url:
            html_tree.make_links_absolute(root_url)
        # ignore the links in the content
        urls = html_tree.xpath('//a/@href')
    # elif "xml" in doc_type: # TODO: Think about this
    # elif "text/plain" in doc_type:
    elif "xml" in doc_type or "text/plain" in doc_type:
        tmp_results = re.findall(URL_REGEX, str_doc)
        urls = [each[0] if "http" in each[0] else "".join(["http://", each[0]])
                for each in results if len(each[0]) > 0]
    else:
        return None
    # TODO: think about where to put the filter level url filtering
    for each_url in urls:
        others = {}
        if handle:
            # pack more options in "param" if need
            each_url, others = handle(each_url, param, opts)
        # A quick dirty check of the duplicate url in the current page
        if len(each_url) == 0 or each_url in url_set:
            continue
        new_job = Job(each_url, others)
        wqueue.put(new_job)
        url_set.add(each_url)
        # An asynchronized dns resolving
        if "domain" in others:
            adns_checker.submit(others["domain"])
    return url_set
