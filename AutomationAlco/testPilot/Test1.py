import unittest, os, test2

#testvar = 'None'
class cMSHParseTest(unittest.TestCase):
    testvar = test2.testFunc()
    #global testvar
    def test_3EncodingChars(self,testvar):
        self.testvar = testvar
        print self.testvar
    def test_AnotherTest(self,testvar):
        self.testvar = testvar
        print self.testvar


if __name__ == '__main__':
    testvar = test2.testFunc()
    unittest.main() 