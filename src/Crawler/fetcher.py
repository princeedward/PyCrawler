import lxml.html as xhtml
from .checker import UrlChecker
from .httpclient import HttpClient, RelativeURIError
from urlhandler import UrlHandler


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

    def __init__(self, url):
        self.url = url
        self.identifier = self.calculateID(self.url)

    def setLastUpdate(self, date):
        self.last_update = date

    def setUrl(self, url):
        self.url = url
        self.identifier = self.calculateID(self.url)

    def calculateID(self, url):
        # TODO: Implement checksum
        pass


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
    job.setUrl(resp_header["content-location"]) # used the real url
    exist, records = UrlChecker(job,param,resp_header)
    if exist:
        monitor.put(Status(200, "Url exists and skiped"))
        return
    # Extract urls and create new jobs, submit dns resolve requests(async)
    headers["Connection"] = "close" # TODO: Think about this, whether this is necessary
    resp_header, content = http_client.request(
        job.url, method="GET", headers=headers)
    UrlExtractor(content, param, doc_type=resp_header["content-type"],
                 handle=UrlHandler,root_url=job.url)
    # do statistics and save the document and statistics (asyn)

    # If job has been finished succesful, indicate the main process
    monitor.put(Status(200))


# A url extractor can extract urls in html/xml/text
# @param str_doc Document in string format
# @param doc_type Document type string
# @param handle Handle funtion wich will be called for each url extracted
# @param root_url Root url for extracting relative urls
# @return True for succeeded, False for fail
def UrlExtractor(str_doc, param, doc_type="html", handle=None, root_url=None):
    if "html" in doc_type:
        html_tree = xhtml.fromstring(str_doc)
        if root_url:
            html_tree.make_links_absolute(root_url)
        # ignore the links in the content
        urls = html_tree.xpath('//a/@href')
        # TODO: think about where to put the filter level url filtering
        if handle:
            for each_url in urls:
                handle(each_url, param) # pack more options in "param" if need
        return True
    elif "xml" in doc_type:
    elif "text/plain" in doc_type:
    else:
        return False
