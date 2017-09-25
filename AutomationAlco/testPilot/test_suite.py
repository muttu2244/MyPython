import unittest,test2

from Test1 import cMSHParseTest


if __name__ == '__main__':
    test_suite = unittest.TestSuite()
    #testvar = test2.testFunc()
    #testvar = test2.testFunc()
    test_suite.addTest(unittest.makeSuite(cMSHParseTest))
    runner=unittest.TextTestRunner()
    runner.run(test_suite)