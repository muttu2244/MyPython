#!/usr/bin/env python2.5

""" Suite file for DHCP Functional test cases """


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
from DHCP_NEG_002 import test_DHCP_NEG_002
#from DHCP_NEG_003 import test_DHCP_NEG_003

if os.environ.has_key('TEST_LOG_DIR'):
    os.mkdir(os.environ['TEST_LOG_DIR'])
    os.chdir(os.environ['TEST_LOG_DIR'])




# build us a log file.  Note console output is enabled.
log = buildLogger("dhcp_suite.log", debug=True)

#!/usr/bin/env python2.5

""" Suite file for DHCP Functional test cases """


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
from DHCP_NEG_002 import test_DHCP_NEG_002
from DHCP_NEG_003 import test_DHCP_NEG_003

if os.environ.has_key('TEST_LOG_DIR'):
    os.mkdir(os.environ['TEST_LOG_DIR'])
    os.chdir(os.environ['TEST_LOG_DIR'])




# build us a log file.  Note console output is enabled.
log = buildLogger("DHCP_NEG_SUITE.log", debug=True)



# build our test suite
suite = test_suite()
suite.addTest(test_DHCP_NEG_002)
suite.addTest(test_DHCP_NEG_003)

# now let's run our test suite
test_runner(stream=sys.stdout).run(suite)
                                                  
