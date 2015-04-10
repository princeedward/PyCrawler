from lxml import etree

# This class is not thread safe for now
class XpathEval:
    # @param xpaths String or list of strings
    def __init__(self, xpaths, superised = True):
        if type(xpaths) is str:
            self.xpath_list_ = [xpaths]
            self.xpath_ = set([xpaths]) # use set to reduce duplicated queries
        elif type(xpaths) is list: # TODO: This condition needs to be enforced
            self.xpath_list_ = xpaths
            self.xpath_ = set(xpaths)
        else:
            raise ValueError("Wrong type of the xpaths argument, it should be \
                              either string or list of strings")
        self.error_superised_ = superised

    # @param doc A string representation of the XML document
    # @return A dictionary where keys are the xpath and values are the tuples of
    #   boolean and match content
    def docMatch(self, doc):
        # Valid XML document
        try:
            root = etree.fromstring(doc)
        except Exception as e:
            if self.error_superised_:
                # do loging
                print e.message()
                return []
            else:
                raise
        return self.domMatch(root)

    # @param root Root node of the lxml element object
    # @return Same as docMatch()
    def domMatch(self, root):
        self.result_ = {}
        for each_path in self.xpath_:
            self.result_[each_path] = self.singleDomMatch(each_path, root)
        return self.result_

    def singleDomMatch(self, xpath_str, root):
        result = root.xpath(xpath_str)
        if result:
            return (True, result)
        else:
            return (False, result)

    @staticmethod
    def singleDocMatch(xpath, doc):
        try:
            root = etree.fromstring(doc)
        except Exception as e:
            if self.error_superised_:
                # do loging
                print e.message()
                return []
            else:
                raise
        result = root.xpath(xpath)
        return result

    # @param index The index of the xpath expression in the list
    # @return
    def isValid(self, index):
        return self.result_[self.xpath_list_[index]][0]

    # TODO: Implement this function when doing the display on the website
    def resultToString(self, result = None):
        pass

    def addXpath(self, xpath_str):
        self.xpath_list_.append(xpath_str)
        self.xpath_.add(xpath_str)

