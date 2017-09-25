import unittest

from clientCalls import *

def suite():
	""" This defines all the tests of a module"""
	suite =unittest.TestSuite()
	suite.addTest(unittest.makeSuite(clientCalls))
	
	return suite

#if __name__ == '__main__':
#        unittest.TextTestRunner(verbosity=2).run(suite())
		
if __name__ == '__main__':
	import testoob
        from testoob.reporting import HTMLReporter
        testoob.main(html='istorage.html', xml='istorage.xml')
