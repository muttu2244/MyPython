#!/usr/bin/env python2.5
### you need to make sure that the libraries are on your path.
### for now we use this hack to get them there.

import sys, os, getopt
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
#from config import *

### import our tests
# REGISTRATION SCRIPTS
'''
from CDR_CLI import test_CDR_CLI
from vgroup_cdr_ports import test_vgroup_ports
from CDR_FUN_001 import test_CDR_FUN_001
from CDR_FUN_002 import test_CDR_FUN_002
from CDR_FUN_003 import test_CDR_FUN_003
from CDR_FUN_004 import test_CDR_FUN_004
from CDR_FUN_005 import test_CDR_FUN_005
from CDR_FUN_006 import test_CDR_FUN_006
from CDR_FUN_007 import test_CDR_FUN_007
from CDR_FUN_010 import test_CDR_FUN_010
from CDR_FUN_012 import test_CDR_FUN_012
from CDR_FUN_013 import test_CDR_FUN_013
from CDR_FUN_015 import test_CDR_FUN_015
from CDR_FUN_016 import test_CDR_FUN_016
from CDR_FUN_017 import test_CDR_FUN_017
from CDR_FUN_018 import test_CDR_FUN_018
from CDR_FUN_019 import test_CDR_FUN_019
from CDR_FUN_020 import test_CDR_FUN_020
from CDR_FUN_026 import test_CDR_FUN_026
from CDR_FUN_030 import test_CDR_FUN_030
from CDR_FUN_031 import test_CDR_FUN_031
from CDR_FUN_032 import test_CDR_FUN_032
from CDR_FUN_033 import test_CDR_FUN_033
from CDR_FUN_034 import test_CDR_FUN_034
from CDR_FUN_036 import test_CDR_FUN_036
from CDR_FUN_037 import test_CDR_FUN_037
from CDR_FUN_038 import test_CDR_FUN_038
from CDR_FUN_039 import test_CDR_FUN_039
from CDR_FUN_040 import test_CDR_FUN_040
from CDR_FUN_041 import test_CDR_FUN_041
'''
from CDR_FUN_042 import test_CDR_FUN_042
from CDR_FUN_043 import test_CDR_FUN_043
from CDR_FUN_045 import test_CDR_FUN_045
from CDR_FUN_053 import test_CDR_FUN_053
from CDR_FUN_056 import test_CDR_FUN_056
from CDR_FUN_057 import test_CDR_FUN_057
#from CDR_FUN_059 import test_CDR_FUN_059
#from CDR_FUN_060 import test_CDR_FUN_060
#from CDR_FUN_061 import test_CDR_FUN_061
#from CDR_FUN_062 import test_CDR_FUN_062
from CDR_FUN_MULTI import test_CDR_FUN_MULTI
from CDR_NEG_001 import test_CDR_NEG_001
from CDR_NEG_002 import test_CDR_NEG_002
#from CDR_NEG_003 import test_CDR_NEG_003
from CDR_NEG_004 import test_CDR_NEG_004
from CDR_NEG_005 import test_CDR_NEG_005
from CDR_HA_FUN_001 import test_CDR_HA_FUN_001
from CDR_HA_FUN_002 import test_CDR_HA_FUN_002
from CDR_HA_FUN_003 import test_CDR_HA_FUN_003
from CDR_HA_FUN_004 import test_CDR_HA_FUN_004
from CDR_HA_FUN_005 import test_CDR_HA_FUN_005

testlogdir = ""
if os.environ.has_key('TEST_LOG_DIR'):
    testlogdir = os.environ['TEST_LOG_DIR']

opts, args = getopt.getopt(sys.argv[1:], "d:")
for o, a in opts:
  if o == "-d":
    testlogdir = a

#  os.mkdir(testlogdir)
if testlogdir != "":
  os.chdir(testlogdir)

# build us a log file.  Note console output is enabled.
log = buildLogger("cdr_suite.log", debug=True,consloe=True)


# build our test suite
suite = test_suite()

#Vgrouping the Topology 
#vgroup_new(vlan_cfg_str)


'''
suite.addTest(test_CDR_CLI)
suite.addTest(test_vgroup_ports)
suite.addTest(test_CDR_FUN_001)
suite.addTest(test_CDR_FUN_002)
suite.addTest(test_CDR_FUN_003)
suite.addTest(test_CDR_FUN_004)
suite.addTest(test_CDR_FUN_005)
suite.addTest(test_CDR_FUN_006)
suite.addTest(test_CDR_FUN_007)
suite.addTest(test_CDR_FUN_010)
suite.addTest(test_CDR_FUN_012)
suite.addTest(test_CDR_FUN_013)
suite.addTest(test_CDR_FUN_015)
suite.addTest(test_CDR_FUN_016)
suite.addTest(test_CDR_FUN_017)
suite.addTest(test_CDR_FUN_018)
suite.addTest(test_CDR_FUN_019)
suite.addTest(test_CDR_FUN_020)
suite.addTest(test_CDR_FUN_026)
suite.addTest(test_CDR_FUN_030)
suite.addTest(test_CDR_FUN_031)
suite.addTest(test_CDR_FUN_032)
suite.addTest(test_CDR_FUN_033)
suite.addTest(test_CDR_FUN_034)
suite.addTest(test_CDR_FUN_036)
suite.addTest(test_CDR_FUN_037)
suite.addTest(test_CDR_FUN_038)
suite.addTest(test_CDR_FUN_039)
suite.addTest(test_CDR_FUN_040)
suite.addTest(test_CDR_FUN_041)
'''
suite.addTest(test_CDR_FUN_042)
suite.addTest(test_CDR_FUN_043)
suite.addTest(test_CDR_FUN_045)
suite.addTest(test_CDR_FUN_053)
suite.addTest(test_CDR_FUN_056)
suite.addTest(test_CDR_FUN_057)
#suite.addTest(test_CDR_FUN_059)
#suite.addTest(test_CDR_FUN_060)	#Less prority test case
#suite.addTest(test_CDR_FUN_061)	#Less prority test case
#suite.addTest(test_CDR_FUN_062)	#Less prority test case
#vgroup_new(vlan_cfg_str1)		#Vgrouping for Multiple sessions : vgroup 3:0 2:1 salvador:e1 huahine:e2
suite.addTest(test_CDR_FUN_MULTI)
suite.addTest(test_CDR_NEG_001)
suite.addTest(test_CDR_NEG_002)
#suite.addTest(test_CDR_NEG_003)
suite.addTest(test_CDR_NEG_004)
suite.addTest(test_CDR_NEG_005)
#vgroup_new(vlan_cfg_str_HA)		#Changing Vgroup qa-tmp2:3:0 takama:e1 for HA
suite.addTest(test_CDR_HA_FUN_001)
suite.addTest(test_CDR_HA_FUN_002)
suite.addTest(test_CDR_HA_FUN_003)
suite.addTest(test_CDR_HA_FUN_004)
suite.addTest(test_CDR_HA_FUN_005)



# now let's run our test suite
test_runner(stream=sys.stdout).run(suite)


