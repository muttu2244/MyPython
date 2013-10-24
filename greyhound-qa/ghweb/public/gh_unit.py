"""This defines and runs all the test suites of iStorage """

import unittest
from blob_unit import *
from scoreboard_unit import *
from delta_unit import *
from blob_diff import *

def suite():
	""" This defines all the tests of a module"""
	suite =unittest.TestSuite()
	suite.addTest(unittest.makeSuite(blob_unit))
	suite.addTest(unittest.makeSuite(scoreboard_unit))
	suite.addTest(unittest.makeSuite(delta_unit))
	suite.addTest(unittest.makeSuite(blob_diff))
	suite.addTest(unittest.makeSuite(iauth_unit.py))
	return suite

#if __name__ == '__main__':
#        unittest.TextTestRunner(verbosity=2).run(suite())
		
if __name__ == '__main__':
	import testoob
        from testoob.reporting import HTMLReporter
        testoob.main(html='istorage.html', xml='istorage.xml')
