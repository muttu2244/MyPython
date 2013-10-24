#!/usr/bin/env python

""" Suite file for Radius Functional test cases """


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
from RADIUS_FUN_001 import test_RADIUS_FUN_001
from RADIUS_FUN_002 import test_RADIUS_FUN_002
from RADIUS_FUN_003 import test_RADIUS_FUN_003
from RADIUS_FUN_004 import test_RADIUS_FUN_004
from RADIUS_FUN_005 import test_RADIUS_FUN_005
from RADIUS_FUN_006 import test_RADIUS_FUN_006
from RADIUS_FUN_007 import test_RADIUS_FUN_007
from RADIUS_FUN_008 import test_RADIUS_FUN_008
from RADIUS_FUN_010 import test_RADIUS_FUN_010
from RADIUS_FUN_011 import test_RADIUS_FUN_011
from RADIUS_FUN_012 import test_RADIUS_FUN_012
from RADIUS_FUN_013 import test_RADIUS_FUN_013
from RADIUS_FUN_014 import test_RADIUS_FUN_014
from RADIUS_FUN_015 import test_RADIUS_FUN_015
from RADIUS_FUN_016 import test_RADIUS_FUN_016
from RADIUS_FUN_017 import test_RADIUS_FUN_017
from RADIUS_FUN_018 import test_RADIUS_FUN_018
from RADIUS_FUN_019 import test_RADIUS_FUN_019
from RADIUS_FUN_020 import test_RADIUS_FUN_020
from RADIUS_FUN_021 import test_RADIUS_FUN_021
from RADIUS_FUN_022 import test_RADIUS_FUN_022
from RADIUS_FUN_023 import test_RADIUS_FUN_023
from RADIUS_FUN_024 import test_RADIUS_FUN_024
from RADIUS_FUN_025 import test_RADIUS_FUN_025
from RADIUS_FUN_026 import test_RADIUS_FUN_026
from RADIUS_FUN_027 import test_RADIUS_FUN_027
from RADIUS_FUN_028 import test_RADIUS_FUN_028
from RADIUS_FUN_029 import test_RADIUS_FUN_029
from RADIUS_FUN_030 import test_RADIUS_FUN_030
from RADIUS_FUN_031 import test_RADIUS_FUN_031
from RADIUS_FUN_032 import test_RADIUS_FUN_032
from RADIUS_FUN_033 import test_RADIUS_FUN_033
from RADIUS_FUN_034 import test_RADIUS_FUN_034
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


#Vgrouping the Topology 
vgroup_new(vlan_cfg_ns)
vgroup_new(vlan_cfg_linux)
vgroup_new(vlan_cfg_radius1)
vgroup_new(vlan_cfg_radius2)



# build our test suite
suite = test_suite()
suite.addTest(test_RADIUS_FUN_001)
suite.addTest(test_RADIUS_FUN_002)
suite.addTest(test_RADIUS_FUN_003)
suite.addTest(test_RADIUS_FUN_004)
suite.addTest(test_RADIUS_FUN_005)
suite.addTest(test_RADIUS_FUN_006)
suite.addTest(test_RADIUS_FUN_007)
suite.addTest(test_RADIUS_FUN_008)
suite.addTest(test_RADIUS_FUN_010)
suite.addTest(test_RADIUS_FUN_011)
suite.addTest(test_RADIUS_FUN_012)
suite.addTest(test_RADIUS_FUN_013)
suite.addTest(test_RADIUS_FUN_014)
suite.addTest(test_RADIUS_FUN_015)
suite.addTest(test_RADIUS_FUN_016)
suite.addTest(test_RADIUS_FUN_017)
suite.addTest(test_RADIUS_FUN_018)
suite.addTest(test_RADIUS_FUN_019)
suite.addTest(test_RADIUS_FUN_020)
suite.addTest(test_RADIUS_FUN_021)
suite.addTest(test_RADIUS_FUN_022)
suite.addTest(test_RADIUS_FUN_023)
suite.addTest(test_RADIUS_FUN_024)
suite.addTest(test_RADIUS_FUN_025)
suite.addTest(test_RADIUS_FUN_026)
suite.addTest(test_RADIUS_FUN_027)
suite.addTest(test_RADIUS_FUN_028)
suite.addTest(test_RADIUS_FUN_029)
suite.addTest(test_RADIUS_FUN_030)
suite.addTest(test_RADIUS_FUN_031)
suite.addTest(test_RADIUS_FUN_032)
suite.addTest(test_RADIUS_FUN_033)
suite.addTest(test_RADIUS_FUN_034)
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

