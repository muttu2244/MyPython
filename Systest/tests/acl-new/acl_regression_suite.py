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
from ACL_PRE_001 import test_ACL_PRE_001
from ACL_FUN_001 import test_ACL_FUN_001
from ACL_FUN_002 import test_ACL_FUN_002
from ACL_FUN_003 import test_ACL_FUN_003
from ACL_FUN_004 import test_ACL_FUN_004
from ACL_FUN_005 import test_ACL_FUN_005
from ACL_FUN_006 import test_ACL_FUN_006
from ACL_FUN_007 import test_ACL_FUN_007
from ACL_FUN_008 import test_ACL_FUN_008
from ACL_FUN_009 import test_ACL_FUN_009
from ACL_FUN_010 import test_ACL_FUN_010
from ACL_FUN_011 import test_ACL_FUN_011
from ACL_FUN_012 import test_ACL_FUN_012
from ACL_FUN_013 import test_ACL_FUN_013
from ACL_FUN_014 import test_ACL_FUN_014
from ACL_FUN_015 import test_ACL_FUN_015
from ACL_FUN_017 import test_ACL_FUN_017
from ACL_FUN_019 import test_ACL_FUN_019
from ACL_FUN_020 import test_ACL_FUN_020
from ACL_FUN_021 import test_ACL_FUN_021
from ACL_FUN_022 import test_ACL_FUN_022
from ACL_FUN_023 import test_ACL_FUN_023
from ACL_FUN_026 import test_ACL_FUN_026
from ACL_FUN_027 import test_ACL_FUN_027
from ACL_FUN_029 import test_ACL_FUN_029
from ACL_FUN_030 import test_ACL_FUN_030
from ACL_FUN_031 import test_ACL_FUN_031
from ACL_FUN_032 import test_ACL_FUN_032
from ACL_FUN_033 import test_ACL_FUN_033
from ACL_FUN_034 import test_ACL_FUN_034
from ACL_FUN_039 import test_ACL_FUN_039
from ACL_FUN_047 import test_ACL_FUN_047
from ACL_FUN_055 import test_ACL_FUN_055
#IPv6 Cases
from ACL_FUN_041 import test_ACL_FUN_041
from ACL_FUN_042 import test_ACL_FUN_042
from ACL_FUN_053 import test_ACL_FUN_053
from ACL_FUN_054 import test_ACL_FUN_054
from ACL_FUN_056 import test_ACL_FUN_056

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
suite.addTest(test_ACL_PRE_001)
suite.addTest(test_ACL_FUN_001)
suite.addTest(test_ACL_FUN_002)
suite.addTest(test_ACL_FUN_003)
suite.addTest(test_ACL_FUN_005)
suite.addTest(test_ACL_FUN_006)
suite.addTest(test_ACL_FUN_007)
suite.addTest(test_ACL_FUN_008)
suite.addTest(test_ACL_FUN_011)
suite.addTest(test_ACL_FUN_012)
suite.addTest(test_ACL_FUN_013)
suite.addTest(test_ACL_FUN_014)
suite.addTest(test_ACL_FUN_017)
suite.addTest(test_ACL_FUN_019)
suite.addTest(test_ACL_FUN_021)
suite.addTest(test_ACL_FUN_026)
suite.addTest(test_ACL_FUN_027)
suite.addTest(test_ACL_FUN_029)
suite.addTest(test_ACL_FUN_030)
suite.addTest(test_ACL_FUN_031)
suite.addTest(test_ACL_FUN_032)
suite.addTest(test_ACL_FUN_033)
suite.addTest(test_ACL_FUN_034)
suite.addTest(test_ACL_FUN_047)
#Session Based Cases 
suite.addTest(test_ACL_FUN_004)
suite.addTest(test_ACL_FUN_009)
suite.addTest(test_ACL_FUN_010)
suite.addTest(test_ACL_FUN_039)

#Egress Case
suite.addTest(test_ACL_FUN_015)
suite.addTest(test_ACL_FUN_020)
suite.addTest(test_ACL_FUN_055)

#Long Run Cases
suite.addTest(test_ACL_FUN_022)
suite.addTest(test_ACL_FUN_023)


#Ipv6 Cases
#suite.addTest(test_ACL_FUN_041)
#suite.addTest(test_ACL_FUN_042)
#suite.addTest(test_ACL_FUN_053)
#suite.addTest(test_ACL_FUN_054)
#suite.addTest(test_ACL_FUN_056)


# add our suite level setup and tear down
suite.setUp = setup
suite.tearDown = teardown

# now let's run our test suite
test_runner(stream=sys.stdout).run(suite)

