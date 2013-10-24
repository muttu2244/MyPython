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
from misc import *
from topo import *


### import our tests
from DHCP_FUN_REL_001 import test_DHCP_FUN_001
from DHCP_FUN_REL_003 import test_DHCP_FUN_003
from DHCP_FUN_REL_004 import test_DHCP_FUN_004
from DHCP_FUN_REL_005 import test_DHCP_FUN_005
from DHCP_FUN_REL_006 import test_DHCP_FUN_006
from DHCP_FUN_REL_007 import test_DHCP_FUN_007
from DHCP_FUN_REL_008 import test_DHCP_FUN_008
from DHCP_FUN_REL_009 import test_DHCP_FUN_009
from DHCP_FUN_REL_014 import test_DHCP_FUN_014
from DHCP_FUN_REL_015 import test_DHCP_FUN_015
from DHCP_FUN_REL_016 import test_DHCP_FUN_016
from DHCP_FUN_REL_017 import test_DHCP_FUN_017
from DHCP_FUN_REL_020 import test_DHCP_FUN_020
from DHCP_FUN_REL_021 import test_DHCP_FUN_021
from DHCP_NEG_002 import test_DHCP_NEG_002
from DHCP_NEG_003 import test_DHCP_NEG_003
from DHCP_CLI_002 import test_DHCP_CLI_002
from DHCP_CLI_016 import test_DHCP_CLI_016
from DHCP_CLI_TESTCASES import test_DHCP_CLI_TESTCASES
from DHCP_DMN_CASES import test_DHCP_DMN_CASES
from DHCP_CLI_009 import test_DHCP_CLI_009
from DHCP_HA_003 import test_DHCP_HA_003
from DHCP_HA_CASES import test_DHCP_HA_CASES


if os.environ.has_key('TEST_LOG_DIR'):
    os.mkdir(os.environ['TEST_LOG_DIR'])
    os.chdir(os.environ['TEST_LOG_DIR'])


# build us a log file.  Note console output is enabled.
log = buildLogger("DHCP_REG_SUITE.log", debug=True)

print "Running Vgroup"
var1 = "%s %s"%(topo1[0],topo1[1])
print var1
vgroup_new(var1)

var2 = "%s %s"%(topo2[0],topo2[1])
print var2
vgroup_new(var2)

var3 = "%s %s"%(topo3[0],topo3[1])
print var3
vgroup_new(var3)

# build our test suite
suite = test_suite()
#suite.addTest(test_DHCP_FUN_001)
#suite.addTest(test_DHCP_FUN_003)
#suite.addTest(test_DHCP_FUN_004)
#suite.addTest(test_DHCP_FUN_005)
suite.addTest(test_DHCP_FUN_006)
suite.addTest(test_DHCP_FUN_007)
suite.addTest(test_DHCP_FUN_008)
suite.addTest(test_DHCP_FUN_009)
#suite.addTest(test_DHCP_FUN_014)
#suite.addTest(test_DHCP_FUN_015)
#suite.addTest(test_DHCP_FUN_016)
#suite.addTest(test_DHCP_FUN_017)
#suite.addTest(test_DHCP_FUN_020)
#suite.addTest(test_DHCP_FUN_021)
#suite.addTest(test_DHCP_NEG_002)
#suite.addTest(test_DHCP_NEG_003)
#suite.addTest(test_DHCP_CLI_002)
#suite.addTest(test_DHCP_CLI_016)
#suite.addTest(test_DHCP_CLI_TESTCASES)
#suite.addTest(test_DHCP_DMN_CASES)
#suite.addTest(test_DHCP_CLI_009)
#suite.addTest(test_DHCP_HA_003)
#suite.addTest(test_DHCP_HA_CASES)

# now let's run our test suite
test_runner(stream=sys.stdout).run(suite)

