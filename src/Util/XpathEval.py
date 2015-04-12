from lxml import etree


# This class is not thread safe for now
# The xpaths stored in the class has to be valid
class XpathEval:

    # @param xpaths String or list of strings
    def __init__(self, xpaths, superised=True):
        if isinstance(xpaths, str):
            if self.validateXpath(xpaths):
                self.xpath_ = set(
                    [xpaths])  # use set to reduce duplicated queries
            else:
                self.xpath_ = set()
        elif isinstance(xpaths, list):
            xpaths = [each for each in xpaths if isinstance(each, str) and
                      self.validateXpath(each)]
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
    def singleDocMatch(xpath, doc, superised=True):
        try:
            root = etree.fromstring(doc)
        except Exception as e:
            if superised:
                # do loging
                print e.message()
                return []
            else:
                raise
        result = root.xpath(xpath)
        return result

    @staticmethod
    def validateXpath(xpath):
        try:
            etree.XPath(xpath)
        except etree.XPathSyntaxError:
            return False
        except etree.XPathEvalError:
            return False
        except Exception:
            raise
        return True

    # @param expression The xpath expression stored to evaluate
    # @return True for
    # TODO: think about the return of invalid expression
    def isValid(self, expression):
        if not self.validateXpath(expression):
            return False
        return self.result_[expression][0]

    # TODO: Implement this function when doing the display on the website
    def resultToString(self, result=None):
        pass

    # @param xpath_str A xpath expression
    # @return True if the string is a valid path expression
    def addXpath(self, xpath_str):
        if not self.validateXpath(xpath_str):
            return False
        self.xpath_list_.append(xpath_str)
        self.xpath_.add(xpath_str)
        return True
