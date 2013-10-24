#!/sr/bin/env python2.5
"""
#######################################################################
#
# Copyright (c) Stoke, Inc.
# All Rights Reserved.
#
# This code is confidential and proprietary to Stoke, Inc. and may only
# be used under a license from Stoke.
#
#######################################################################

DESCRIPTION: Verify the output changed for show fabric and show fabric counters
TEST PLAN:   Global_Cli_TestPlan
TEST CASES:  Global_Cli_014

TOPOLOGY DIAGRAM: 

DEPENDENCIES: None
How to run: "python2.5 Global_Cli_014"
AUTHOR: npatel
REVIEWER: 
"""

import sys, os
import  time


mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

# Frame-work libraries 
from SSX import * 
from log import *
from logging import getLogger
from StokeTest import test_case, test_suite, test_runner  
from helpers import is_healthy
from ShowCmdList import *
from topo import *
#from config import *
import pexpect
import re

class test_Global_Cli_014(test_case):
    myLog = getLogger()

    def setUp(self):

        #Establish a telnet session to SSX with 4.6B2
        self.ssx = SSX(ssx['ipaddr'])
        self.ssx.telnet()
       

    def tearDown(self):
        # Close the telnet session of SSX
        self.ssx.close()
    
    def test_Global_Cli_014(self):
        switch_over = True
        status = True
	
	res=self.ssx.cmd("show fabric")
	if "Slot Model" not in res:
                self.myLog.output("show fabric command is not working")
                status = False


        for i in range(2,5):
            ret = self.ssx.cmd("show fabric counters slot %s" %i)
            #for line in ret.split("\n"):
            if "Link  Rx bits/sec    Rx frames/sec  Rx % Tx bits/sec    Tx frames/sec  Tx %" not in ret:
	    	self.myLog.output("show fabric counters command is not working")
	        status = False


        self.failUnless(status,"Failed testcase Global_cli_014.py")

if __name__ == '__main__':

    filename = os.path.split(__file__)[1].replace('.py','.log')
    log = buildLogger(filename, debug=True, console=True)
    suite = test_suite()
    suite.addTest(test_Global_Cli_014)
    test_runner().run(suite)
