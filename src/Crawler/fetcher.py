# This class indicate the status of the fetcher
class Status:

    # @param code Indicate the child process status
    #               200 Ready for job
    def __init__(self, code):
        self.status = code


# This class is the job class which including the url to crawl and other
# information to boost the crawling
class Job:

    def __init__(self, url):
        self.url = url


# Fetcher function which runs in each child process
def Fetcher(job, param, works, monitor):
    # If job has been finished succesful, indicate the main process
    monitor.put(Status(200))
