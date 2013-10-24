#!/usr/bin/env python

""" Suite file for RADIUS negative test cases """


### you need to make sure that the libraries are on your path.
import sys, os

mydir = os.path.dirname(__file__)
precom_file = __file__
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)


### import the libraries we need.
from log import *
from topo import *
from misc import *


#from log import buildLogger
from StokeTest import test_suite, test_runner

### import our tests
#from RADIUS_NEG_001 import test_RADIUS_NEG_001
from RADIUS_NEG_002 import test_RADIUS_NEG_002
from RADIUS_NEG_003 import test_RADIUS_NEG_003
from RADIUS_NEG_004 import test_RADIUS_NEG_004
#from RADIUS_NEG_005 import test_RADIUS_NEG_005
from RADIUS_NEG_006 import test_RADIUS_NEG_006


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



#Vgrouping the Topology 
vgroup_new(vlan_cfg_ns)
vgroup_new(vlan_cfg_linux)
vgroup_new(vlan_cfg_radius1)
vgroup_new(vlan_cfg_radius2)


# build our test suite
suite = test_suite()
#suite.addTest(test_RADIUS_NEG_001)
suite.addTest(test_RADIUS_NEG_002)
suite.addTest(test_RADIUS_NEG_003)
suite.addTest(test_RADIUS_NEG_004)
#suite.addTest(test_RADIUS_NEG_005)
suite.addTest(test_RADIUS_NEG_006)


# add our suite level setup and tear down
suite.setUp = setup
suite.tearDown = teardown

# now let's run our test suite
test_runner().run(suite)

