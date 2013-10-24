#!/usr/bin/env python2.5

""" Suite file for DoCoMo Use cases """

### you need to make sure that the libraries are on your path.
import sys, os

mydir = os.path.dirname(__file__)
precomfile =__file__
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)


### import the libraries we need.
#from log import *
from log import buildLogger
from StokeTest import test_suite, test_runner

### import our tests
from DoCoMo_4_2_2 import test_DoCoMo_4_2_2
from DoCoMo_4_3_1 import test_DoCoMo_4_3_1
from DoCoMo_5_2_1 import test_DoCoMo_5_2_1
from DoCoMo_6_1_2 import test_DoCoMo_6_1_2
from DoCoMo_6_2_1 import test_DoCoMo_6_2_1
from DoCoMo_6_2_5 import test_DoCoMo_6_2_5
from DoCoMo_6_2_6 import test_DoCoMo_6_2_6
from DoCoMo_7_1_1 import test_DoCoMo_7_1_1
from DoCoMo_7_14_1 import test_DoCoMo_7_14_1
from DoCoMo_7_14_2 import test_DoCoMo_7_14_2
from DoCoMo_7_5_1 import test_DoCoMo_7_5_1
from DoCoMo_7_6_1 import test_DoCoMo_7_6_1
from DoCoMo_8_1_1 import test_DoCoMo_8_1_1
from DoCoMo_8_3_6 import test_DoCoMo_8_3_6
from DoCoMo_PERF_GLCR_SESS_003 import test_DoCoMo_PERF_GLCR_SESS_003
from DoCoMo_PERF_NONGLCR_006 import test_DoCoMo_PERF_NONGLCR_006
from GLCR_SES_IKEv2_FUN_001 import test_GLCR_SES_IKEv2_FUN_001
from GLCR_SES_IKEv2_FUN_007 import test_GLCR_SES_IKEv2_FUN_007
from GLCR_SES_IKEv2_FUN_035 import test_GLCR_SES_IKEv2_FUN_035
from GLCR_SES_IKEv2_FUN_036 import test_GLCR_SES_IKEv2_FUN_036
from GLCR_SES_IKEv2_FUN_037 import test_GLCR_SES_IKEv2_FUN_037

if os.environ.has_key('TEST_LOG_DIR'):
    os.mkdir(os.environ['TEST_LOG_DIR'])
    os.chdir(os.environ['TEST_LOG_DIR'])


# build us a log file.  Note console output is enabled.
log = buildLogger("DoCoMo_SUITE.log", debug=True)

# build our test suite
suite = test_suite()
suite.addTest(test_DoCoMo_4_2_2)
suite.addTest(test_DoCoMo_4_3_1)
suite.addTest(test_DoCoMo_5_2_1)
suite.addTest(test_DoCoMo_6_1_2)
suite.addTest(test_DoCoMo_6_2_1)
suite.addTest(test_DoCoMo_6_2_5)
suite.addTest(test_DoCoMo_6_2_6)
suite.addTest(test_DoCoMo_7_1_1)
suite.addTest(test_DoCoMo_7_14_1)
suite.addTest(test_DoCoMo_7_14_2)
suite.addTest(test_DoCoMo_7_5_1)
suite.addTest(test_DoCoMo_7_6_1)
suite.addTest(test_DoCoMo_8_1_1)
suite.addTest(test_DoCoMo_8_3_6)
suite.addTest(test_DoCoMo_PERF_GLCR_SESS_003)
suite.addTest(test_DoCoMo_PERF_NONGLCR_006)
suite.addTest(test_GLCR_SES_IKEv2_FUN_001)
suite.addTest(test_GLCR_SES_IKEv2_FUN_007)
suite.addTest(test_GLCR_SES_IKEv2_FUN_035)
suite.addTest(test_GLCR_SES_IKEv2_FUN_036)
suite.addTest(test_GLCR_SES_IKEv2_FUN_037)


# now let's run our test suite
test_runner().run(suite)

