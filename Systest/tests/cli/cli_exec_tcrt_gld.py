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
DESCRIPTION             : This script will invoke CLI-Driver script command for SSX-Commands
REFERENCE               : SSX-CLI Test and Automation Strategy
TEST CASES              : cli_exec_tcrt
TOPOLOGY DIAGRAM        :

         ----------                        -----------                          -----------
        | Python   |                      |           |                        |           |
        |Framework |----------------------| CLI Tool  |------------------------|    SSX    |
         ----------                        -----------                          -----------



AUTHOR                  : Alok Mohapatra ; email:alok@primesoftsolutionsinc.com
REVIEWER                :
DEPENDENCIES            : CLI-driver tool
DATE			: 25th April 2007
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

class cli_exec_tcrt_gld(test_case):
   
    myLog=getLogger()

    def setUp(self):
      
        #Establish telnet session for connecting to SSX and checking its status
        self.myLog.output("Trying to connect to SSX ")
	self.ssx = SSX(topo.ssx1['ip_addr'])
	self.ssx.telnet()
        self.ssx.clear_health_stats()

    def tearDown(self):
        #Closing down the telnet sessions
        self.ssx.close()
	self.myLog.output("All The Telnet Sessions Closed Successfully")

    def test_cli_exec_tcrt(self):
        """Starting Test Case Steps"""
      
	# Running the CLI-driver commnad
	 
	os.system(" cli-driver.pl -l %(gldn_fldr)s/gld_tcrt_exec_%(ssx_ver)s.log -u %(ssx_user)s -p %(ssx_pw)s -C traceroute -f %(drvr-data)s %(ssx)s " %script_var)    	

	self.myLog.output("Golden log file created Succesfully")
        
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		


if __name__ == '__main__':

    # Build A log File.  Note Console Output Is Enabled.
    filename = os.path.split(__file__)[1].replace('.py','.log')
    log = buildLogger(filename, debug=True, console=True)

    # Build The Test Suite And Run It.
    suite = test_suite()
    suite.addTest(cli_exec_tcrt_gld)
    test_runner().run(suite)
    
