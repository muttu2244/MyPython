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
DESCRIPTION             : This script will invoke "context local -> interface " on SSX CLI (Configuration mode)
REFERENCE               : SSX-CLI Test and Automation Strategy
TEST CASES              : ipsc_001_pos, 
                          ipsc_002_rae,
                          ipsc_003_ere,
                          ipsc_004_rm2,
                          ipsc_005_all 
TOPOLOGY DIAGRAM        :

        |------------------|                       
        | Python Framework |                         |-----------|
        |------------------|-------------------------|    SSX    |
        | CLI Driver Tool  |                         |-----------|
        |------------------|

AUTHOR                  : Alok Mohapatra ; email:@primesoftsolutionsinc.com
REVIEWER                :
DEPENDENCIES            : cli-driver.pl (A STOKE internal tool, CVS:systest/util/cli-driver/)
UPDATE DATE             : 7th May 2007
"""

### Importing system libraries 
import sys, os, re
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

class cli_hid2_conf(test_case):
   
    myLog = getLogger()  

    def setUp(self):
      
        #Establish telnet session for connecting to SSX and checking its status
	self.ssx = SSX(topo.ssx_con['ip_addr'])
	self.ssx.telnet()
        self.ssx.clear_health_stats()

    def tearDown(self):
        #Closing down the telnet sessions
        self.ssx.close()
	self.myLog.output("All The Telnet Sessions Closed Successfully")

    ####################################################################

    def test_hid2_ctst_pos(self):
        """Starting Test Case Steps"""
      
	# Running the cli-driver commnad
	os.system(" cli-driver.pl -l %(cli_fldr)s/cntx_hid2_pos_%(ssx_ver)s.log -u %(ssx_user)s -p %(ssx_pw)s -S 2 -i cli-test -f %(drvr-data_hid2)s -c %(ssx_system)s " %script_var)    	
	
        # Comparing the log file against the golden file
	#self.myLog.output("Comparing the log files")
	#diff_out = os.system("diff %(gldn_fldr)s/gld_cntx_ipsc_pos_%(ssx_ver)s.log  %(cli_fldr)s/cntx_ipsc_pos_%(ssx_ver)s.log" %script_var )	
	# Declaring Test result according to diff output
	#self.failUnless(not diff_out ,"Test Fail due to mismatch in logs")	
        
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		

    ####################################################################



if  __name__== '__main__':

    # Build A log File.  Note Console Output Is Enabled.
    filename = os.path.split(__file__)[1].replace('.py','.log')
    log = buildLogger(filename, debug=True, console=True)

    # Build The Test Suite And Run It.
    suite = test_suite()
    suite.addTest(cli_hid2_conf)
    test_runner().run(suite)
    
