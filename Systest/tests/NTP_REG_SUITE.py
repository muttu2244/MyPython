#!/usr/bin/env python2.5

""" Suite file for ntp Functional test cases """


### you need to make sure that the libraries are on your path.
import sys, os

mydir = os.path.dirname(__file__)
precom_file = __file__
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)


### import the libraries we need.
from log import buildLogger
from StokeTest import test_suite, test_runner

### import our tests
from NTP_FUN_001 import test_NTP_FUN_001
from NTP_FUN_004 import test_NTP_FUN_004
from NTP_FUN_006 import test_NTP_FUN_006
from NTP_FUN_007 import test_NTP_FUN_007
from NTP_FUN_010 import test_NTP_FUN_010
from NTP_FUN_011 import test_NTP_FUN_011
from NTP_FUN_012 import test_NTP_FUN_012
from NTP_FUN_013 import test_NTP_FUN_013

if os.environ.has_key('TEST_LOG_DIR'):
    os.mkdir(os.environ['TEST_LOG_DIR'])
    os.chdir(os.environ['TEST_LOG_DIR'])




# build us a log file.  Note console output is enabled.
log = buildLogger("ntp_suite.log", debug=True)



# build our test suite
suite = test_suite()
suite.addTest(test_NTP_FUN_001)
suite.addTest(test_NTP_FUN_004)
suite.addTest(test_NTP_FUN_006)
suite.addTest(test_NTP_FUN_007)
suite.addTest(test_NTP_FUN_010)
suite.addTest(test_NTP_FUN_011)
suite.addTest(test_NTP_FUN_012)
suite.addTest(test_NTP_FUN_013)


# now let's run our test suite
test_runner(stream=sys.stdout).run(suite)

