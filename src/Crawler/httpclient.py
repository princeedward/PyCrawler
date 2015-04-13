import httplib2


# A future more sophiscated implementation must implement
# httplib2.Http interface
class HttpClient(httplib2.Http):
    pass


RelativeURIError = httplib2.RelativeURIError
