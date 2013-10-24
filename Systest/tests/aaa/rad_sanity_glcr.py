#!/usr/bin/env python2.5

""" Suite file for Radius Functional test cases """


### you need to make sure that the libraries are on your path.
import sys, os, getopt

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
from vgroup_aaa_ports import test_vgroup_ports
from RADIUS_FUN_001 import test_RADIUS_FUN_001
from RADIUS_FUN_003 import test_RADIUS_FUN_003
from RADIUS_FUN_015 import test_RADIUS_FUN_015
from RADIUS_FUN_017 import test_RADIUS_FUN_017
from RADIUS_FUN_030 import test_RADIUS_FUN_030
from RADIUS_NEG_002 import test_RADIUS_NEG_002

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

testlogdir = ""
if os.environ.has_key('TEST_LOG_DIR'):
    testlogdir = os.environ['TEST_LOG_DIR']

opts, args = getopt.getopt(sys.argv[1:], "d:")
for o, a in opts:
  if o == "-d":
    testlogdir = a

if testlogdir != "":
  os.mkdir(testlogdir)
  os.chdir(testlogdir)

# build us a log file.  Note console output is enabled.
log = buildLogger("suite.log", debug=True)


#Vgrouping the Topology 
'''
vgroup_new(vlan_cfg_ns)
vgroup_new(vlan_cfg_linux)
vgroup_new(vlan_cfg_radius1)
vgroup_new(vlan_cfg_radius2)
'''


# build our test suite
suite = test_suite()
suite.addTest(test_vgroup_ports)
suite.addTest(test_RADIUS_FUN_001)
suite.addTest(test_RADIUS_FUN_003)
suite.addTest(test_RADIUS_FUN_015)
suite.addTest(test_RADIUS_FUN_017)
suite.addTest(test_RADIUS_FUN_030)
suite.addTest(test_RADIUS_NEG_002)



# add our suite level setup and tear down
suite.setUp = setup
suite.tearDown = teardown

# now let's run our test suite
test_runner(stream=sys.stdout).run(suite)

