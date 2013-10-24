#!/usr/bin/env python2.5

""" Suite file for AAA Functional test cases """


### you need to make sure that the libraries are on your path.
import sys, os, getopt, time

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

time.sleep(10)
### import our tests
from AAA_CLI	 import test_AAA_CLI
from vgroup_aaa_ports import test_vgroup_ports
from AAA_FUN_001 import test_AAA_FUN_001
from AAA_FUN_002 import test_AAA_FUN_002
from AAA_FUN_003 import test_AAA_FUN_003
from AAA_FUN_004 import test_AAA_FUN_004
from AAA_FUN_005 import test_AAA_FUN_005
from AAA_FUN_006 import test_AAA_FUN_006
from AAA_FUN_007 import test_AAA_FUN_007
from AAA_FUN_008 import test_AAA_FUN_008
from AAA_FUN_009 import test_AAA_FUN_009
from AAA_FUN_010 import test_AAA_FUN_010
from AAA_FUN_011 import test_AAA_FUN_011
from AAA_FUN_012 import test_AAA_FUN_012
from AAA_FUN_013 import test_AAA_FUN_013
from AAA_FUN_015 import test_AAA_FUN_015
from AAA_FUN_016 import test_AAA_FUN_016
from AAA_FUN_017 import test_AAA_FUN_017
from AAA_FUN_018 import test_AAA_FUN_018
from AAA_FUN_019 import test_AAA_FUN_019
from AAA_FUN_020 import test_AAA_FUN_020
from AAA_FUN_021 import test_AAA_FUN_021
from AAA_FUN_022 import test_AAA_FUN_022
from AAA_FUN_023 import test_AAA_FUN_023
from AAA_FUN_024 import test_AAA_FUN_024
from AAA_FUN_025 import test_AAA_FUN_025
from AAA_FUN_026 import test_AAA_FUN_026
from AAA_FUN_027 import test_AAA_FUN_027
from AAA_FUN_028 import test_AAA_FUN_028
from AAA_FUN_029 import test_AAA_FUN_029
from AAA_FUN_030 import test_AAA_FUN_030
from AAA_FUN_031 import test_AAA_FUN_031
from AAA_FUN_032 import test_AAA_FUN_032

from AAA_NEG_001 import test_AAA_NEG_001
from AAA_NEG_002 import test_AAA_NEG_002
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

#  os.mkdir(testlogdir)
if testlogdir != "":
  os.chdir(testlogdir)

# build us a log file.  Note console output is enabled.
#log = buildLogger("suite.log", debug=True,console=True)
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
suite.addTest(test_AAA_CLI)
suite.addTest(test_vgroup_ports)
suite.addTest(test_AAA_FUN_001)
suite.addTest(test_AAA_FUN_002)
suite.addTest(test_AAA_FUN_003)
suite.addTest(test_AAA_FUN_004)
suite.addTest(test_AAA_FUN_005)
suite.addTest(test_AAA_FUN_006)
suite.addTest(test_AAA_FUN_007)
suite.addTest(test_AAA_FUN_008)
suite.addTest(test_AAA_FUN_009)
suite.addTest(test_AAA_FUN_010)
suite.addTest(test_AAA_FUN_011)
suite.addTest(test_AAA_FUN_012)
suite.addTest(test_AAA_FUN_013)
suite.addTest(test_AAA_FUN_015)
suite.addTest(test_AAA_FUN_016)
suite.addTest(test_AAA_FUN_017)
suite.addTest(test_AAA_FUN_018)
suite.addTest(test_AAA_FUN_019)
suite.addTest(test_AAA_FUN_020)
suite.addTest(test_AAA_FUN_021)
suite.addTest(test_AAA_FUN_022)
suite.addTest(test_AAA_FUN_023)
suite.addTest(test_AAA_FUN_024)
suite.addTest(test_AAA_FUN_025)
suite.addTest(test_AAA_FUN_026)
suite.addTest(test_AAA_FUN_027)
suite.addTest(test_AAA_FUN_028)
suite.addTest(test_AAA_FUN_029)
suite.addTest(test_AAA_FUN_030)
suite.addTest(test_AAA_FUN_031)
suite.addTest(test_AAA_FUN_032)

suite.addTest(test_AAA_NEG_001)
suite.addTest(test_AAA_NEG_002)
suite.addTest(test_AAA_NEG_003)


# add our suite level setup and tear down
suite.setUp = setup
suite.tearDown = teardown


# now let's run our test suite
test_runner(stream=sys.stdout).run(suite)

