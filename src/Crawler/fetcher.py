from .checker import UrlChecker
from .httpclient import HttpClient, RelativeURIError


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

    def setLastUpdate(self, date):
        self.last_update = date


def CheckContentType(type_str, allowed_types):
    for each_type in allowed_types:
        if type_str.find(each_type) >= 0:
            return True
    return False


USER_AGENT = "penn/cis455/crawler/0.1"

# Fetcher function which runs in each child process
def Fetcher(job, param, works, monitor):
    # document size and document type check using response header
    # better with persistence connection
    http_client = HttpClient()
    headers = {"User-Agent": USER_AGENT,
               "Connection": "keep-alive",
               }
    try:
        resp_header, content = http_client.request(
            job.url, method="HEAD", headers=headers)
    except RelativeURIError:
        monitor.put(Status(401, "Url is not absolute"))
        return
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
    # check the existence of the url last update (politeness handled by queue)
    exist, records = UrlChecker(job)
    # Extract urls and create new jobs, submit dns resolve requests(async)

    # do statistics and save the document and statistics (asyn)

    # If job has been finished succesful, indicate the main process
    monitor.put(Status(200))
