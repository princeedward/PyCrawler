from urlparse import urlparse


# This is enhenced urlparser to handle the string wihtout protocol
# @param url_str A string needs to be parsed
# @return An object same as the return of urlparse()
def urlParser(url_str):
    colon_pos = url_str.find("://")
    if colon_pos > 0:
        slash_pos = url_str.find("/", 0, colon_pos)
        if slash_pos >= 0:
            url_str = "".join(["http://", url_str])
    elif colon_pos == 0:
        url_str = "".join(["http", url_str])
    else:
        url_str = "".join(["http://", url_str])
    parsed_uri = urlparse(url_str)
    return parsed_uri
