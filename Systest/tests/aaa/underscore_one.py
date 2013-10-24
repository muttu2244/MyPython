#!/usr/bin/env python

""" Suite file for IKEv2 Functional test cases """


### you need to make sure that the libraries are on your path.
import sys, os

mydir = os.path.dirname(__file__)
precom_file = __file__
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)


### import the libraries we need.
from log import *
#from log import buildLogger
from StokeTest import test_suite, test_runner

### import our tests
from RADIUS_FUN_007_1 import test_RADIUS_FUN_007_1
from RADIUS_FUN_008_1 import test_RADIUS_FUN_008_1
from RADIUS_FUN_010_1 import test_RADIUS_FUN_010_1
from RADIUS_FUN_011_1 import test_RADIUS_FUN_011_1
from RADIUS_FUN_012_1 import test_RADIUS_FUN_012_1
from RADIUS_FUN_013_1 import test_RADIUS_FUN_013_1
from RADIUS_FUN_014_1 import test_RADIUS_FUN_014_1
from RADIUS_FUN_015_1 import test_RADIUS_FUN_015_1
from RADIUS_FUN_016_1 import test_RADIUS_FUN_016_1
from RADIUS_FUN_024_1 import test_RADIUS_FUN_024_1
from RADIUS_FUN_030_1 import test_RADIUS_FUN_030_1


def setup():
    """Simulated suite setup."""
    log.info("This is where your suite setup method would run.")
    log.debug("This is where your suite setup method would run.")
    print "This is where your suite setup method would run."

def teardown():
    """Simulated suite cleanup."""
    log.info("This is where your suite teardown method would run.")
    log.debug("This is where your suite teardown method would run.")
    print "This is where your suite teardown method would run."

# build us a log file.  Note console output is enabled.
log = buildLogger("suite.log", debug=True, console=True)





# build our test suite
suite = test_suite()
suite.addTest(test_RADIUS_FUN_007_1)
suite.addTest(test_RADIUS_FUN_008_1)
suite.addTest(test_RADIUS_FUN_010_1)
suite.addTest(test_RADIUS_FUN_011_1)
suite.addTest(test_RADIUS_FUN_012_1)
suite.addTest(test_RADIUS_FUN_013_1)
suite.addTest(test_RADIUS_FUN_014_1)
suite.addTest(test_RADIUS_FUN_015_1)
suite.addTest(test_RADIUS_FUN_016_1)
suite.addTest(test_RADIUS_FUN_024_1)
suite.addTest(test_RADIUS_FUN_030_1)



# add our suite level setup and tear down
suite.setUp = setup
suite.tearDown = teardown

# now let's run our test suite
test_runner().run(suite)

