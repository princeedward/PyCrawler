from checker import UrlChecker


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


# Fetcher function which runs in each child process
def Fetcher(job, param, works, monitor):
    # check the existence of the url last update (politeness handled by queue)

    # document size and document type check using response header
    # better with persistence connection

    # Extract urls and create new jobs, submit dns resolve requests(async)

    # do statistics and save the document and statistics (asyn)

    # If job has been finished succesful, indicate the main process
    monitor.put(Status(200))
