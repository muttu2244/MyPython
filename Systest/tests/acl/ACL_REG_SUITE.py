#!/usr/bin/env python2.5

""" Suite file for acl Functional test cases """


### you need to make sure that the libraries are on your path.
import sys, os

mydir = os.path.dirname(__file__)
precom_file = __file__
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)


### import the libraries we need.
#from log import *
from log import buildLogger
from StokeTest import test_suite, test_runner

### import our tests
from ACL_FUN_006 import test_ACL_FUN_006
from ACL_FUN_007 import test_ACL_FUN_007
from ACL_FUN_008 import test_ACL_FUN_008
from ACL_FUN_009 import test_SAN_ACL_009
from ACL_FUN_010 import test_SAN_ACL_010
from ACL_FUN_011_PERMITUDP import test_SAN_ACL_PERMITUDP
from ACL_FUN_011_PERMITTCP import test_SAN_ACL_PERMITTCP
from ACL_FUN_011_PERMITIGMP import test_SAN_ACL_PERMITIGMP
from ACL_FUN_012_DENYICMP import test_SAN_ACL_DENYICMP
from ACL_FUN_012_DENYUDP import test_SAN_ACL_DENYUDP 
from ACL_FUN_011_PERMITICMP import test_SAN_ACL_PERMITICMP
from ACL_FUN_012_DENYTCP import test_SAN_ACL_DENYTCP
from ACL_FUN_012_DENYIGMP import test_SAN_ACL_DENYIGMP
from ACL_FUN_013 import test_SAN_ACL_013
from ACL_FUN_014 import test_SAN_ACL_014
from ACL_FUN_015 import test_SAN_ACL_015
from ACL_FUN_016 import test_SAN_ACL_016
from ACL_FUN_017 import test_SAN_ACL_017
from ACL_FUN_024 import test_ACL_FUN_024
from ACL_FUN_034 import test_ACL_FUN_034

if os.environ.has_key('TEST_LOG_DIR'):
    os.mkdir(os.environ['TEST_LOG_DIR'])
    os.chdir(os.environ['TEST_LOG_DIR'])




# build us a log file.  Note console output is enabled.
log = buildLogger("ACL_REG_SUITE.log", debug=True)



# build our test suite
suite = test_suite()
suite.addTest(test_ACL_FUN_006)
suite.addTest(test_ACL_FUN_007)
suite.addTest(test_ACL_FUN_008)
suite.addTest(test_SAN_ACL_009)
suite.addTest(test_SAN_ACL_010)
suite.addTest(test_SAN_ACL_PERMITIGMP)
suite.addTest(test_SAN_ACL_PERMITUDP)
suite.addTest(test_SAN_ACL_PERMITTCP)
suite.addTest(test_SAN_ACL_DENYICMP)
suite.addTest(test_SAN_ACL_DENYUDP)
suite.addTest(test_SAN_ACL_PERMITICMP)
suite.addTest(test_SAN_ACL_DENYTCP)
suite.addTest(test_SAN_ACL_DENYIGMP)
suite.addTest(test_SAN_ACL_013)
suite.addTest(test_SAN_ACL_014)
suite.addTest(test_SAN_ACL_015)
suite.addTest(test_SAN_ACL_016)
suite.addTest(test_SAN_ACL_017)
uite.addTest(test_ACL_FUN_024)
suite.addTest(test_ACL_FUN_034)

# now let's run our test suite
test_runner(stream=sys.stdout).run(suite)

