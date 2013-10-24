#!/usr/bin/env python2.5

""" Suite file for ip-ip Functional test cases """


### you need to make sure that the libraries are on your path.
import sys, os, getopt

mydir = os.path.dirname(__file__)
precom_file = __file__

qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)


### import the libraries we need.
#from log import *
from log import buildLogger
from StokeTest import test_suite, test_runner

### import our tests

from ACL_FUN_009 import test_ACL_FUN_009
from ACL_FUN_010 import test_ACL_FUN_010
from ACL_FUN_014 import test_ACL_FUN_014
from ACL_FUN_015 import test_ACL_FUN_015
from ACL_FUN_017 import test_ACL_FUN_017
#suite.addTest(test_ACL_FUN_013)

# now let's run our test suite
test_runner(stream=sys.stdout).run(suite)

