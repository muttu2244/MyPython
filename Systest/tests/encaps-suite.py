#!/usr/bin/env python2.5

"""Encaps Suite."""


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
from logging import getLogger
from StokeTest import test_suite, test_runner

### import our tests
from encaps import encaps

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

#log = buildLogger('encaps_suite.log' )
log = buildLogger('encaps_suite.log', debug=True)

# build our test suite
suite = test_suite()
suite.addTest(encaps)


# now let's run our test suite
test_runner(stream=sys.stdout).run(suite)
