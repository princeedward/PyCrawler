from lxml import etree

def xpathMatch(xpath, doc):
    root = etree.fromstring(doc)
    if type(xpath) is list:
        result = []
        for each_path in xpath:
            result.append(xpathEval(each_path, root))
        return result
    else:
        return xpathEval(xpath,root)

# @param xpath A single xpath expression string
# @param root Root node of the lxml element object
def xpathEval(xpath, root):
    pass
