#!/usr/bin/env python2.5

""" Suite file for AAA Functional test cases """


### you need to make sure that the libraries are on your path.
import sys, os, getopt

mydir = os.path.dirname(__file__)
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
from AAA_FUN_001 import test_AAA_FUN_001
from AAA_FUN_002 import test_AAA_FUN_002
from AAA_FUN_004 import test_AAA_FUN_004
from AAA_FUN_008 import test_AAA_FUN_008
from AAA_FUN_011 import test_AAA_FUN_011
from AAA_FUN_015 import test_AAA_FUN_015
from AAA_FUN_017 import test_AAA_FUN_017
from AAA_FUN_021 import test_AAA_FUN_021
from AAA_NEG_001 import test_AAA_NEG_001
from AAA_NEG_003 import test_AAA_NEG_003


def setup():
    """Simulated suite setup."""
    log.info("This is where your suite setup method would run.")
    log.debug("This is where your suite setup method would run.")

def teardown():
    """Simulated suite cleanup."""
    log.info("This is where your suite teardown method would run.")
    log.debug("This is where your suite teardown method would run.")

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
suite.addTest(test_AAA_FUN_001)
suite.addTest(test_AAA_FUN_002)
suite.addTest(test_AAA_FUN_004)
suite.addTest(test_AAA_FUN_008)
suite.addTest(test_AAA_FUN_011)
suite.addTest(test_AAA_FUN_015)
suite.addTest(test_AAA_FUN_017)
suite.addTest(test_AAA_FUN_021)
suite.addTest(test_AAA_NEG_001)
suite.addTest(test_AAA_NEG_003)

# add our suite level setup and tear down
suite.setUp = setup
suite.tearDown = teardown

# now let's run our test suite
test_runner(stream=sys.stdout).run(suite)

