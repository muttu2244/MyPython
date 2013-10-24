#!/usr/bin/env python

""" Suite file for dos-attacks Functional test cases """


### you need to make sure that the libraries are on your path.
import sys, os

mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)


### import the libraries we need.
from log import *
#from log import buildLogger
from StokeTest import test_suite, test_runner

### import our tests
from ip_atk_003 import test_ip_atk_003
from ip_atk_004 import test_ip_atk_004
from ip_atk_005 import test_ip_atk_005
from ip_atk_006 import test_ip_atk_006
from ip_atk_007 import test_ip_atk_007
from ip_atk_008 import test_ip_atk_008
from ip_atk_007 import test_ip_atk_007
from ip_atk_009 import test_ip_atk_009
from ip_atk_010 import test_ip_atk_010
from ip_atk_013 import test_ip_atk_013
from ip_atk_016 import test_ip_atk_016
from ip_atk_017 import test_ip_atk_017
from ip_atk_019 import test_ip_atk_019
from ip_atk_021 import test_ip_atk_021
from ip_atk_023 import test_ip_atk_023
from ip_atk_024 import test_ip_atk_024
from ip_atk_025 import test_ip_atk_025
from ip_atk_026 import test_ip_atk_026
from ip_atk_027 import test_ip_atk_027
from ip_atk_028 import test_ip_atk_028
from ip_atk_033 import test_ip_atk_033
from ip_atk_034 import test_ip_atk_034
from ip_atk_035 import test_ip_atk_035
from ip_atk_036 import test_ip_atk_036
from ip_atk_037 import test_ip_atk_037
from ip_atk_038 import test_ip_atk_038
from ip_atk_039 import test_ip_atk_039
from ip_atk_040 import test_ip_atk_040
from ip_atk_041 import test_ip_atk_041
from ip_atk_042 import test_ip_atk_042
from ip_atk_043 import test_ip_atk_043
from ip_atk_049 import test_ip_atk_049
from ip_atk_050 import test_ip_atk_050 
from ip_atk_052 import test_ip_atk_052
from ip_atk_053 import test_ip_atk_053
from ip_atk_054 import test_ip_atk_054
from ip_atk_055 import test_ip_atk_055
from ip_atk_056 import test_ip_atk_056
from ip_atk_057 import test_ip_atk_057
from ip_atk_058 import test_ip_atk_058
from ip_atk_059 import test_ip_atk_059
from ip_atk_062 import test_ip_atk_062
from ip_atk_063 import test_ip_atk_063
from ip_atk_064 import test_ip_atk_064
from ip_atk_065 import test_ip_atk_065
from ip_atk_066 import test_ip_atk_066
from ip_atk_067 import test_ip_atk_067
from ip_atk_068 import test_ip_atk_068
from ip_atk_076 import test_ip_atk_076
from ip_atk_077 import test_ip_atk_077
from ip_atk_078 import test_ip_atk_078
from ip_atk_079 import  test_ip_atk_079
from ip_atk_082 import  test_ip_atk_082
from ip_atk_084 import  test_ip_atk_084 
from ip_atk_087 import  test_ip_atk_087


if os.environ.has_key('TEST_LOG_DIR'):
    os.mkdir(os.environ['TEST_LOG_DIR'])
    os.chdir(os.environ['TEST_LOG_DIR'])

# build us a log file.  Note console output is enabled.
log = buildLogger("DOS_REGRESSION_SUITE.log", debug=True)



# build our test suite
suite = test_suite()
suite.addTest(test_ip_atk_003)
suite.addTest(test_ip_atk_004)
suite.addTest(test_ip_atk_005)
suite.addTest(test_ip_atk_006)
suite.addTest(test_ip_atk_007)
suite.addTest(test_ip_atk_008)
suite.addTest(test_ip_atk_009)
suite.addTest(test_ip_atk_010)
suite.addTest(test_ip_atk_013)
suite.addTest(test_ip_atk_016)
suite.addTest(test_ip_atk_017)
suite.addTest(test_ip_atk_016)
suite.addTest(test_ip_atk_019)
suite.addTest(test_ip_atk_021)
suite.addTest(test_ip_atk_023)
suite.addTest(test_ip_atk_024)
suite.addTest(test_ip_atk_025)
suite.addTest(test_ip_atk_026)
suite.addTest(test_ip_atk_027)
suite.addTest(test_ip_atk_028)
suite.addTest(test_ip_atk_033)
suite.addTest(test_ip_atk_034)
suite.addTest(test_ip_atk_035)
suite.addTest(test_ip_atk_036)
suite.addTest(test_ip_atk_037)
suite.addTest(test_ip_atk_038)
suite.addTest(test_ip_atk_039)
suite.addTest(test_ip_atk_040)
suite.addTest(test_ip_atk_041)
suite.addTest(test_ip_atk_042)
suite.addTest(test_ip_atk_043)
suite.addTest(test_ip_atk_049)
suite.addTest(test_ip_atk_050)
suite.addTest(test_ip_atk_052)
suite.addTest(test_ip_atk_053)
suite.addTest(test_ip_atk_054)
suite.addTest(test_ip_atk_055)
suite.addTest(test_ip_atk_056)
suite.addTest(test_ip_atk_057)
suite.addTest(test_ip_atk_058)
suite.addTest(test_ip_atk_059)
suite.addTest(test_ip_atk_062)
suite.addTest(test_ip_atk_063)
suite.addTest(test_ip_atk_064)
suite.addTest(test_ip_atk_065)
suite.addTest(test_ip_atk_066)
suite.addTest(test_ip_atk_067)
suite.addTest(test_ip_atk_068)
suite.addTest(test_ip_atk_076)
suite.addTest(test_ip_atk_077)
suite.addTest(test_ip_atk_078)
suite.addTest(test_ip_atk_079)
suite.addTest(test_ip_atk_082)
suite.addTest(test_ip_atk_084)
suite.addTest(test_ip_atk_087)






#Now let's run our test suite
test_runner(stream=sys.stdout).run(suite)


