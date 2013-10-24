#!/usr/bin/env python

""" Suite file for dos-attacks Functional test cases """


### you need to make sure that the libraries are on your path.
import sys, os

mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)


### import the libraries we need.
#from log import *
from log import buildLogger
from StokeTest import test_suite, test_runner

### import our tests
from ip_atk_008 import test_ip_atk_008
from ip_atk_009 import test_ip_atk_009
from ip_atk_010 import test_ip_atk_010
from ip_atk_017 import test_ip_atk_017
from ip_atk_024 import test_ip_atk_024
from ip_atk_026 import test_ip_atk_026
from ip_atk_027 import test_ip_atk_027
from ip_atk_028 import test_ip_atk_028
from ip_atk_034 import test_ip_atk_034
from ip_atk_040 import test_ip_atk_040
from ip_atk_049 import test_ip_atk_049
from ip_atk_076 import test_ip_atk_076
from ip_atk_087 import test_ip_atk_087


if os.environ.has_key('TEST_LOG_DIR'):
    os.mkdir(os.environ['TEST_LOG_DIR'])
    os.chdir(os.environ['TEST_LOG_DIR'])

# build us a log file.  Note console output is enabled.
log = buildLogger("DOS_SANITY_SUITE.log", debug=True)



# build our test suite
suite = test_suite()
suite.addTest(test_ip_atk_008)
suite.addTest(test_ip_atk_009)
suite.addTest(test_ip_atk_010)
suite.addTest(test_ip_atk_017)
suite.addTest(test_ip_atk_024)
suite.addTest(test_ip_atk_026)
suite.addTest(test_ip_atk_027)
suite.addTest(test_ip_atk_028)
suite.addTest(test_ip_atk_034)
suite.addTest(test_ip_atk_040)
suite.addTest(test_ip_atk_049)
suite.addTest(test_ip_atk_076)
suite.addTest(test_ip_atk_087)


#Now let's run our test suite
test_runner(stream=sys.stdout).run(suite)


