#!/usr/bin/env python2.5
### you need to make sure that the libraries are on your path.
### for now we use this hack to get them there.

import sys, os
mydir = os.path.dirname(__file__)
precom_file = __file__
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)


### import the libraries we need.
from log import buildLogger
from log import *
from StokeTest import test_suite, test_runner
#from topo import *
#from config import *

### import our tests
# REGISTRATION SCRIPTS

from vgroup_cdr_ports import test_vgroup_ports 
from CDR_FUN_001 import test_CDR_FUN_001
from CDR_FUN_010 import test_CDR_FUN_010
from CDR_FUN_020 import test_CDR_FUN_020
from CDR_FUN_030 import test_CDR_FUN_030
from CDR_FUN_037 import test_CDR_FUN_037

if os.environ.has_key('TEST_LOG_DIR'):
    os.mkdir(os.environ['TEST_LOG_DIR'])
    os.chdir(os.environ['TEST_LOG_DIR'])

# build us a log file.  Note console output is enabled.
log = buildLogger("cdr_suite.log", debug=True )


# build our test suite
suite = test_suite()
suite.addTest(test_vgroup_ports)
suite.addTest(test_CDR_FUN_001)
suite.addTest(test_CDR_FUN_010)
suite.addTest(test_CDR_FUN_020)
suite.addTest(test_CDR_FUN_030)
suite.addTest(test_CDR_FUN_037)

# now let's run our test suite
test_runner(stream=sys.stdout).run(suite)

