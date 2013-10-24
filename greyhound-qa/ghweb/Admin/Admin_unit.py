from user_blob_delete import *
from user_blob_revert_golden import *
from user_history_get  import *
from meta_threshold_get import *
from reputation_get import *
from payments_meta_get import *
from reputation_update import * 

def suites():
        suite =unittest.TestSuite()
	suite.addTest(unittest.makeSuite(golden_revert_class))
	suite.addTest(unittest.makeSuite(blob_delete_class))
	suite.addTest(unittest.makeSuite(history_get_class))
	suite.addTest(unittest.makeSuite(meta_threshold_get))
	suite.addTest(unittest.makeSuite(reputation_get))	
	suite.addtest(unittest.makesuite(admin_payments_get_class))
	suite.addtest(unittest.makesuite(admin_reputation_update))


if __name__ == '__main__':
        import testoob
        from testoob.reporting import HTMLReporter
        testoob.main(html='/opt/zynga/greyhound/current/tests/scripts/test/results/admin_unit.html')




