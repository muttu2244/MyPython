import unittest
import testoob
from mqs_auth import mqs_auth
from mqs_graph_auth import mqs_graph_auth
from mqs_graph_testcases import mqs_graph_testcases
from mqs_meta_testcases import mqs_meta_testcases

def suite():
	suite = unittest.TestSuite()
	suite.addTests(unittest.makeSuite(mqs_auth))
	suite.addTests(unittest.makeSuite(mqs_graph_auth))
	suite.addTests(unittest.makeSuite(mqs_graph_testcases))
	suite.addTests(unittest.makeSuite(mqs_meta_testcases))
	return suite

if __name__ == '__main__':
	import testoob
	suite()
	from testoob.reporting import HTMLReporter
	testoob.main(html='mqs.html', xml='mqs.xml')
