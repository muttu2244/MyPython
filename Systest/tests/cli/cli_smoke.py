#!/usr/bin/env python2.5

#######################################################################
#
# Copyright (c) Stoke, Inc.
# All Rights Reserved.
#
# This code is confidential and proprietary to Stoke, Inc. and may only
# be used under a license from Stoke.
#
#######################################################################

"""
DESCRIPTION             : This script will invoke smoke test for CLI commnads 
REFERENCE               :
TEST CASES              : cli_smok_test
TOPOLOGY DIAGRAM        :

        |------------------|                       
        | Python Framework |                         |-----------|
        |------------------|-------------------------|    SSX    |
        | CLI Driver Tool  |                         |-----------|
        |------------------|


AUTHOR                  : Alok Mohapatra ; email:alok@primesoftsolutionsinc.com
REVIEWER                :
DEPENDENCIES            : 
DATE			: 25th May 2007
"""


### Importing system libraries 
import sys, os, getopt, re
import time
mydir = os.path.dirname(__file__)
precom_file = __file__
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

### Importing libraries from the python framework
from Linux import Linux
from log import buildLogger
from logging import getLogger
from StokeTest import test_case, test_suite, test_runner
from SSX import SSX
from helpers import is_healthy

### Importing topo file and Config file
import topo
from config import *
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


class cli_smok_test(test_case):
   
    myLog = getLogger()  

    def setUp(self):
      
        #Establish telnet session for connecting to SSX and checking its status
        self.myLog.output("Trying to connect to SSX ")
	self.ssx = SSX(topo.ssx_con['ip_addr'])
	self.ssx.telnet()
        #self.ssx.clear_health_stats()

    def tearDown(self):
        #Closing down the telnet sessions
        self.ssx.close()
	self.myLog.output("All The Telnet Sessions Closed Successfully")

    def test_cli_smok_crash(self):
        """Starting Test Case Steps"""
        
        # Getting the SSX version
        ssx_vrsn = self.ssx.get_version()
        script_var['ssx_ver']= ssx_vrsn['branch']

        # Getting the required cli-driver.pl script option according to SSX connection type(console or managemnt)
        if   "con" in topo.ssx_system['ip_addr']:
                cli_dvr_optn  = "-z"

        elif self.ssx._isnfs():
                cli_dvr_optn  = ""

        else:
                cli_dvr_optn  = " -u %(ssx_user)s -p %(ssx_pw)s " % script_var

        # Pushing the var(cli-driver.pl script option) value into the script_var variable
        script_var['ssx_type']=cli_dvr_optn

        # closing the SSX connection
        self.ssx.close()


	# Running the cli-driver commnad
	cli_return = os.system(" cli-driver.pl -s -l smoke_test_%(ssx_ver)s.log  %(ssx_type)s -n -2 -a -f /volume/labtools/systest/tests/cli/smoke_cfg -c %(ssx_system)s" %script_var)    	
	

	# Opening SSX connection
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()
        
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs, Warn_logs=100), "Platform is not healthy")		


    def test_cli_smok_dupl(self):

	#closing SSX conenction
        self.ssx.close()
	
	# Running the cli-driver commnad
        cli_return = os.system(" cli-driver.pl -s -l smoke_test_%(ssx_ver)s.log  %(ssx_type)s -n -r -2 -a -f /volume/labtools/systest/tests/cli/smoke_cfg -c %(ssx_system)s" %script_var)

        # verifying  the CLI driver's  return value
        self.failUnless(cli_return == 0, "Fail due to unacceptance of duplicate cli comamnd twice")

	# Opening SSX connection
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()

        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs, Warn_logs=100), "Platform is not healthy")

if __name__ == '__main__':

    # Build A log File.  Note Console Output Is Enabled.
    filename = os.path.split(__file__)[1].replace('.py','.log')
    log = buildLogger(filename, debug=True)

    # Build The Test Suite And Run It.
    suite = test_suite()
    suite.addTest(cli_smok_test)
    test_runner(stream=sys.stdout).run(suite)
 
