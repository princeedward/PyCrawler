from XpathEval import XpathEval
import unittest


class XpathEval_test(unittest.TestCase):

    def test_constructor(self):
        with self.assertRaises(ValueError):
            XpathEval(5)
        xpath_eval = XpathEval([])
        self.assertTrue(xpath_eval.error_superised_)
        try:
            xpath_eval = XpathEval("/foo/bar")
        except ValueError:
            self.fail("XpathEval cannot be initialized with a single string")
        else:
            self.assertIs(type(xpath_eval.xpath_), set)
            self.assertEqual(len(xpath_eval.xpath_), 1)

    def test_document_1(self):
        f = open('test/test_xml_1.xml', 'r')
        self.xml_doc_1 = f.read()
        f.close()
        test_paths = ["/imas/production",
                      ]
        xpath_eval = XpathEval(test_paths)
        self.assertTrue(XpathEval.singleDocMatch(test_paths[0], self.xml_doc_1))
        self.assertTrue(xpath_eval.docMatch(self.xml_doc_1))


def main():
    unittest.main()

if __name__ == '__main__':
    main()
