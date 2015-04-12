from django.shortcuts import render
# from django.http import HttpResponse
# from django.template import RequestContext, loader
import httplib
from Util.UrlParser import urlParser as urlparser
from Util.XpathEval import XpathEval

# Create your views here.
DOC_MAX_SIZE = 35000000


def index(request):
    return render(request, 'xpathEvaluation/index.html', {})


def xeval(request):
    xpath_eval = request.GET['xpath_string']
    if not XpathEval.validateXpath(xpath_eval):
        return render(request, 'xpathEvaluation/index.html', {'message':
                                                              'Invalid xpath'})
    doc_url = request.GET['document_url']
    parsed_uri = urlparser(doc_url)
    if parsed_uri.scheme == "http":
        conn = httplib.HTTPConnection(parsed_uri.netloc)
    elif parsed_uri.scheme == "https":
        conn = httplib.HTTPSConnection(parsed_uri.netloc)
    else:
        conn.close()
        return render(request, 'xpathEvaluation/index.html', {'message':
                                                              'Invalid url'})
    try:
        conn.connect()
    except Exception:
        conn.close()
        return render(
            request, 'xpathEvaluation/index.html',
            {'message': 'Service does not exist'})
    # Check the content-type first
    conn.request("HEAD", parsed_uri.path)
    res = conn.getresponse()
    doc_type = res.getheader("content-type", None)
    if doc_type is None:
        conn.close()
        return render(
            request, 'xpathEvaluation/index.html',
            {'message': 'Unrecognized content'})
    elif doc_type.find("xml") >= 0:
        # Check the size of the document
        doc_size = res.getheader("content-length", None)
        if doc_size is None or float(doc_size) <= DOC_MAX_SIZE:
            conn.close()
            if parsed_uri.scheme == "http":
                conn = httplib.HTTPConnection(parsed_uri.netloc)
            elif parsed_uri.scheme == "https":
                conn = httplib.HTTPSConnection(parsed_uri.netloc)
            conn.request("GET", parsed_uri.path)
            res = conn.getresponse()
        else:
            conn.close()
            return render(
                request, 'xpathEvaluation/index.html',
                {'message': 'Document is too large'})
        xml_doc_str = res.read()
    else:
        conn.close()
        return render(
            request, 'xpathEvaluation/index.html',
            {'message': 'Not a xml document'})
    result = XpathEval.singleDocMatch(xpath_eval, xml_doc_str)
    if result:
        return render(request, 'xpathEvaluation/index.html', {'message':
                                                              'True'})
    else:
        return render(request, 'xpathEvaluation/index.html', {'message':
                                                              'False'})
