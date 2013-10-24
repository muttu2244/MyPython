from archive_queue_fetch import *
from archive_queue_update import *
from credibility_get import *
#from dau_queue_fetch import *
from dau_queue_update import *
from fraud_update import *
from history_update import *
from payments_meta_get import *
from reputation_update import *
from thresholds_fetch import *
from thresholds_update import *
from user_blob_archive import *
from user_blob_revert import *
from user_golden_blob_update import *
import unittest

def suites():
	suite =unittest.TestSuite()
	suite.addTest(unittest.makeSuite(archive_fetch))
	suite.addTest(unittest.makeSuite(archive_queue_update))
	suite.addTest(unittest.makeSuite(credibility_get))
	suite.addTest(unittest.makeSuite(dau_fetch))
	suite.addTest(unittest.makeSuite(dau_update_class))
	#suite.addTest(unittest.makeSuite(fraud_update_class))
	suite.addTest(unittest.makeSuite(history_update))
	suite.addTest(unittest.makeSuite(payments_get_class))
	suite.addTest(unittest.makeSuite(reputation_update))
	suite.addTest(unittest.makeSuite(thresholds_fetch))
	suite.addTest(unittest.makeSuite(thresholds_update))
	suite.addTest(unittest.makeSuite(archive_blob))
	suite.addTest(unittest.makeSuite(revert_blob))
	suite.addTest(unittest.makeSuite(golden_update_class))
	return suite

if __name__ == '__main__':
	import testoob
	from testoob.reporting import HTMLReporter
	testoob.main(html='/opt/zynga/greyhound/current/gh_test/scripts/test/results/internal_unit.html')
