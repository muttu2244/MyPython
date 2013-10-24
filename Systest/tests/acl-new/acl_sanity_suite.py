#!/usr/bin/env python2.5

""" Suite file for ACL Functional test cases """


### you need to make sure that the libraries are on your path.
import sys, os, getopt

mydir = os.path.dirname(__file__)
precom_file = __file__
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)


### import the libraries we need.
from log import *
#from log import buildLogger
from StokeTest import test_suite, test_runner

#For Vgroup
from topo import *
from misc import vgroup_new

### import our tests
#from ACL_PRE_001 import test_ACL_PRE_001
from ACL_FUN_001 import test_ACL_FUN_001
from ACL_FUN_002 import test_ACL_FUN_002
from ACL_FUN_017 import test_ACL_FUN_017
from ACL_FUN_021 import test_ACL_FUN_021
from ACL_FUN_027 import test_ACL_FUN_027
from ACL_FUN_030 import test_ACL_FUN_030
from ACL_FUN_042 import test_ACL_FUN_042

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
log = buildLogger("suite.log", debug=True,consloe=True)

#Vgrouping Required Equipment
vgroup_new(vlan_cfg_acl)
vgroup_new(vlan_cfg_acl2)

# build our test suite
suite = test_suite()
#suite.addTest(test_ACL_PRE_001)
suite.addTest(test_ACL_FUN_001)
suite.addTest(test_ACL_FUN_002)
suite.addTest(test_ACL_FUN_017)
suite.addTest(test_ACL_FUN_021)
suite.addTest(test_ACL_FUN_027)
suite.addTest(test_ACL_FUN_030)
suite.addTest(test_ACL_FUN_042)


# add our suite level setup and tear down
suite.setUp = setup
suite.tearDown = teardown

# now let's run our test suite
test_runner(stream=sys.stdout).run(suite)

