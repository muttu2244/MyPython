#!/usr/bin/env python2.5

""" Suite file for DoCoMo regression test cases """

### you need to make sure that the libraries are on your path.
import sys, os

mydir = os.path.dirname(__file__)
precomfile =__file__
qa_lib_dir = os.path.join(mydir, "../../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

# Import topo and config information
#from topo_doc import *
#from ospf_config_doc import *

### import the libraries we need.
from log import buildLogger
from StokeTest import test_suite, test_runner
#from testopiaIf import *
from config import *
### import our tests

from ACL_Func_072 import test_ACL_Func_072
from ACL_Func_211 import test_ACL_FUNC_211



if os.environ.has_key('TEST_LOG_DIR'):
    os.mkdir(os.environ['TEST_LOG_DIR'])
    os.chdir(os.environ['TEST_LOG_DIR'])


# build us a log file.  Note console output is enabled.
log = buildLogger("acl_SUITE_temp.log", debug=True)


#build our test suite
suite = test_suite()

suite.addTest(test_ACL_Func_072)
suite.addTest(test_ACL_FUNC_211)

# now let's run our test suite
test_runner().run(suite)







